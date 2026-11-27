/* DenoiseOpt crowdsourced listening test: static page, no external libraries, no cookies, no analytics.
 * URL (Prolific): index.html?stage=main|screener&PROLIFIC_PID={{%PROLIFIC_PID%}}&STUDY_ID={{%STUDY_ID%}}&SESSION_ID={{%SESSION_ID%}}
 * Sessions come from sessions/sNNN.json produced by scripts/session_builder.py.
 * Nothing is sent anywhere until the participant finishes; the endpoint and completion codes are placeholders. */
"use strict";
const CONFIG = {
  sessionsBase: "sessions/",
  nSessions: 60,
  resultEndpoint: "",                       // e.g. an EU-hosted collector URL (see ../collector/schema.sql); empty = download JSON only
  completionUrlMain: "https://app.prolific.com/submissions/complete?cc=REPLACE_WITH_MAIN_STUDY_CODE",
  completionUrlScreenerPass: "https://app.prolific.com/submissions/complete?cc=REPLACE_WITH_SCREENER_PASS_CODE",
  completionUrlScreenerFail: "https://app.prolific.com/submissions/complete?cc=REPLACE_WITH_SCREENER_FAIL_CODE",
  headphoneTrials: 6, headphonePass: 5,
};
const DCR_LABELS = {5:"Degradation is inaudible",4:"Degradation is audible but not annoying",3:"Degradation is slightly annoying",2:"Degradation is annoying",1:"Degradation is very annoying"};
const q = new URLSearchParams(location.search);
const STAGE = q.get("stage") === "screener" ? "screener" : "main";
const PID = q.get("PROLIFIC_PID") || "", STUDY = q.get("STUDY_ID") || "", PSESSION = q.get("SESSION_ID") || "";
const app = document.getElementById("app");
const out = { stage: STAGE, pid: PID, study_id: STUDY, prolific_session: PSESSION, started: new Date().toISOString(), answers: [], questionnaire: {}, headphone: null, sampleRate: null };
let actx = null;

function h(html){ app.innerHTML = html; }
function btn(label, id, extra=""){ return `<button id="${id}" ${extra}>${label}</button>`; }
function fnv1a(s){ let x=0x811c9dc5; for(const c of s){ x^=c.charCodeAt(0); x=Math.imul(x,0x01000193)>>>0; } return x>>>0; }
function ctx(){ if(!actx){ actx = new (window.AudioContext||window.webkitAudioContext)(); out.sampleRate = actx.sampleRate; } return actx; }
const sleep = ms => new Promise(r => setTimeout(r, ms));

function playUrl(url){
  return new Promise((resolve, reject) => {
    const a = new Audio(url); a.preload = "auto";
    a.onended = () => resolve(); a.onerror = () => reject(new Error("audio failed: " + url));
    a.play().catch(reject);
  });
}
function playTone(freq, seconds, gain, antiphase){
  const c = ctx(), n = Math.floor(c.sampleRate*seconds), buf = c.createBuffer(2, n, c.sampleRate);
  const L = buf.getChannelData(0), R = buf.getChannelData(1), ramp = Math.floor(0.05*c.sampleRate);
  for(let i=0;i<n;i++){
    const env = Math.min(1, i/ramp, (n-1-i)/ramp), v = gain*env*Math.sin(2*Math.PI*freq*i/c.sampleRate);
    L[i] = v; R[i] = antiphase ? -v : v;
  }
  const s = c.createBufferSource(); s.buffer = buf; s.connect(c.destination); s.start();
  return new Promise(r => { s.onended = r; });
}

/* ---------- screens ---------- */
function consent(){
  h(`<div class="box"><h2>Information and consent</h2>
  <p>I am Julian M. Kleber, an independent researcher (contact: julian.m.kleber@gmail.com). This short study asks you to listen to
  3-second synthesizer tones (a musical note with slight vibrato) through headphones and rate how noticeable clicks, buzzing or other disturbances are.
  There is no known risk beyond ordinary listening; please keep the volume comfortable.</p>
  <p>We collect your Prolific ID, your ratings and answers, timing, and a few non-identifying questions about your listening setup.
  We do not ask for your name, e-mail, or location, and we do not store your IP address or cookies. Your Prolific ID is used only to pay you and to
  detect duplicate or careless submissions; it is replaced by a random code after payment is complete and is never published.
  Results are published only in aggregated, anonymous form, and the anonymous data set may be shared openly.
  Taking part is voluntary; you can stop at any time by closing the page (you then return the study on Prolific). Full privacy notice: see the study description.</p>
  <label><input type="checkbox" id="c1"> I am at least 18 years old, I have read the information above, and I agree to take part.</label><br>
  ${btn("Continue","go","disabled")}</div>`);
  const c = document.getElementById("c1"), g = document.getElementById("go");
  c.onchange = () => g.disabled = !c.checked;
  g.onclick = () => { ctx().resume(); volume(); };
}
function volume(){
  h(`<div class="box"><h2>Headphones and volume</h2>
  <p>Please use wired or wireless headphones or earphones (no loudspeakers), in a quiet room. Press play and set your volume so the tone is clearly audible but comfortable.
  Do not raise it afterwards: some test sounds contain short clicks that can be louder than the tone.</p>
  ${btn("Play test tone","tone")} <span class="muted">(about 1 second)</span><br>${btn("Continue","next")}</div>`);
  document.getElementById("tone").onclick = () => playTone(440, 1.0, 0.1, false);
  document.getElementById("next").onclick = () => (STAGE === "screener" ? headphoneCheck() : loadSession());
}
async function headphoneCheck(){
  let correct = 0; out.headphone = {trials: []};
  for(let t=0;t<CONFIG.headphoneTrials;t++){
    const target = Math.floor(Math.random()*3), anti = [0,1,2].filter(i=>i!==target)[Math.floor(Math.random()*2)];
    h(`<div class="box"><h2>Headphone check ${t+1} / ${CONFIG.headphoneTrials}</h2><p>You will hear three tones. Which one was the <b>quietest</b>? (Each trial plays once.)</p><p id="st">Playing...</p>
    ${[1,2,3].map(i=>btn(`Tone ${i}`,`a${i}`,"disabled")).join("")}</div>`);
    for(let i=0;i<3;i++){ await playTone(200, 1.0, i===target?0.05:0.1, i===anti); await sleep(500); }
    document.getElementById("st").textContent = "Choose now.";
    const pick = await new Promise(res => [1,2,3].forEach(i => { const b=document.getElementById(`a${i}`); b.disabled=false; b.onclick=()=>res(i-1); }));
    out.headphone.trials.push({target, anti, pick}); if(pick===target) correct++;
  }
  out.headphone.correct = correct; out.headphone.passed = correct >= CONFIG.headphonePass;
  await questionnaire();
}
async function questionnaire(){
  await new Promise(res => {
    h(`<div class="box"><h2>A few questions about your setup</h2>
    <p>Device: <select id="dev"><option>over-ear headphones</option><option>in-ear / earbuds</option><option>on-ear headphones</option><option>other</option></select></p>
    <p>Room: <select id="room"><option>quiet</option><option>some background noise</option><option>noisy</option></select></p>
    <p>Do you have any hearing difficulty? <select id="hear"><option>no</option><option>yes</option><option>prefer not to say</option></select></p>
    <p>Years of experience with music production or audio engineering: <input id="exp" type="number" min="0" max="80" value="0" style="width:4rem"></p>
    <p class="muted">Optional comment (please do not enter personal data): <br><textarea id="free" rows="2" style="width:100%"></textarea></p>
    ${btn("Finish","fin")}</div>`);
    document.getElementById("fin").onclick = () => { out.questionnaire = {device:dev.value, room:room.value, hearing:hear.value, experience_years:+exp.value, comment:free.value}; res(); };
  });
  await finish();
}
let SESSION = null;
async function loadSession(){
  const k = PID ? fnv1a(PID) % CONFIG.nSessions : Math.floor(Math.random()*CONFIG.nSessions);
  try{ SESSION = await (await fetch(`${CONFIG.sessionsBase}s${String(k).padStart(3,"0")}.json`)).json(); }
  catch(e){ h(`<p>Could not load the study material. Please return the study on Prolific.</p>`); return; }
  out.session_index = k; instructions();
}
function instructions(){
  h(`<div class="box"><h2>Task</h2>
  <p>Each trial plays two 3-second tones: first the <b>reference</b> (a clean tone), then the <b>test</b> tone. Rate how much the test tone is degraded compared with the reference,
  focusing on clicks, ticks, buzzing or roughness. Some test tones are identical to the reference.</p>
  <p>Scale: 5 ${DCR_LABELS[5]} - 4 ${DCR_LABELS[4]} - 3 ${DCR_LABELS[3]} - 2 ${DCR_LABELS[2]} - 1 ${DCR_LABELS[1]}.</p>
  <p>You first do ${SESSION.training.length} practice trials, then ${SESSION.dcr.length} rating trials and ${SESSION.ab.length} short comparisons. About 15 to 17 minutes. Some trials check that you are listening; please answer them honestly.</p>
  ${btn("Start practice","go")}</div>`);
  document.getElementById("go").onclick = () => runItems(SESSION.training, "train").then(() => runItems(SESSION.dcr, "dcr")).then(() => runAB(SESSION.ab)).then(questionnaire);
}
async function runItems(items, mode){
  for(let i=0;i<items.length;i++){
    const it = items[i];
    h(`<progress max="${items.length}" value="${i}"></progress><div class="box"><h2>${mode==="train"?"Practice":"Rating"} ${i+1} / ${items.length}</h2>
    <p id="st">Press play: reference, then test.</p>${btn("Play","play")}
    <div class="scale">${[5,4,3,2,1].map(v=>`<button data-v="${v}" disabled>${v} - ${DCR_LABELS[v]}</button>`).join("")}</div></div>`);
    let plays = 0, tEnable = 0;
    const playBtn = document.getElementById("play"), rate = [...document.querySelectorAll(".scale button")];
    const answer = new Promise(res => rate.forEach(b => b.onclick = () => res(+b.dataset.v)));
    playBtn.onclick = async () => {
      playBtn.disabled = true; document.getElementById("st").textContent = "Reference...";
      try{ await playUrl(it.ref); await sleep(500); document.getElementById("st").textContent = "Test..."; await playUrl(it.test); }
      catch(e){ document.getElementById("st").textContent = "Playback failed, please check your audio and press play again."; playBtn.disabled=false; return; }
      plays++; document.getElementById("st").textContent = "Rate the test tone."; rate.forEach(b=>b.disabled=false); playBtn.disabled=false; playBtn.textContent="Play again"; if(!tEnable) tEnable = performance.now();
    };
    const v = await answer;
    out.answers.push({type: mode==="train"?"train":it.type, tile: it.tile, system: it.system, rating: v, expected: it.expected, plays, rt_ms: Math.round(performance.now()-tEnable)});
  }
}
async function runAB(items){
  for(let i=0;i<items.length;i++){
    const it = items[i];
    h(`<progress max="${items.length}" value="${i}"></progress><div class="box"><h2>Comparison ${i+1} / ${items.length}</h2>
    <p id="st">Press play: you will hear clip 1, then clip 2. Which one has fewer clicks or other disturbances?</p>${btn("Play","play")}<br>
    ${btn("Clip 1 has fewer","first","disabled")}${btn("Clip 2 has fewer","second","disabled")}${btn("No audible difference","none","disabled")}</div>`);
    let plays = 0, tEnable = 0;
    const playBtn = document.getElementById("play"), opts = ["first","second","none"].map(id=>document.getElementById(id));
    const answer = new Promise(res => opts.forEach(b => b.onclick = () => res(b.id)));
    playBtn.onclick = async () => {
      playBtn.disabled = true;
      try{ document.getElementById("st").textContent="Clip 1..."; await playUrl(it.a_url); await sleep(700); document.getElementById("st").textContent="Clip 2..."; await playUrl(it.b_url); }
      catch(e){ document.getElementById("st").textContent="Playback failed, press play again."; playBtn.disabled=false; return; }
      plays++; document.getElementById("st").textContent="Choose."; opts.forEach(b=>b.disabled=false); playBtn.disabled=false; playBtn.textContent="Play again"; if(!tEnable) tEnable=performance.now();
    };
    const c = await answer;
    out.answers.push({type:"ab", tile:it.tile, first:it.first, second:it.second, choice:c, plays, rt_ms: Math.round(performance.now()-tEnable)});
  }
}
async function finish(){
  out.finished = new Date().toISOString();
  let sent = false;
  if(CONFIG.resultEndpoint){
    try{ const r = await fetch(CONFIG.resultEndpoint, {method:"POST", headers:{"content-type":"application/json"}, body: JSON.stringify(out)}); sent = r.ok; }catch(e){ sent = false; }
  }
  const url = STAGE==="main" ? CONFIG.completionUrlMain : (out.headphone && out.headphone.passed ? CONFIG.completionUrlScreenerPass : CONFIG.completionUrlScreenerFail);
  if(sent){ h(`<div class="box"><h2>Thank you</h2><p>Your answers were saved.</p><p><a href="${url}">Return to Prolific to complete the study</a></p></div>`); }
  else{
    const blob = URL.createObjectURL(new Blob([JSON.stringify(out)], {type:"application/json"}));
    h(`<div class="box"><h2>Almost done</h2><p>Your answers could not be sent automatically. Please download the file and keep it, then continue; do not edit it.</p>
    <p><a download="listening_result.json" href="${blob}">Download answers</a></p><p><a href="${url}">Return to Prolific</a></p></div>`);
  }
}
consent();
