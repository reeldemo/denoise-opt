# Participant information, consent and privacy notice (English, DRAFT for Julian's approval)

Status: draft. Not reviewed by a data-protection officer or an ethics committee. Replace bracketed items before launch.
Prolific requires a clear privacy notice for studies that process personal data, and Prolific IDs count as pseudonymous personal data under GDPR.

## 1. Who is running the study (controller)

Julian M. Kleber, independent researcher, [postal address for the notice: to be filled in by Julian; do not put private data in the repository], e-mail julian.m.kleber@gmail.com. ORCID 0000-0001-5518-0932.
There is no institution and no data-protection officer. Julian is the data controller.

## 2. What the study is

You listen to short (3 s) synthesizer tones through headphones and rate how noticeable clicks, buzzing or other disturbances are
(about 4 minutes screening, about 17 minutes main study). The study compares algorithms that repair loop-point clicks in wavetable synthesis.
There is no deception. The sounds are not harmful; please keep the volume comfortable and stop if anything is uncomfortable.

## 3. What data is collected, why and on which legal basis

| Data | Purpose | Retention |
|---|---|---|
| Prolific ID (pseudonymous), study and session IDs | payment, duplicate and fraud control | deleted/replaced by a random code within 30 days after the last payment is approved |
| Ratings, choices, response times, number of plays | the research question | kept as anonymous data (after the ID is replaced) |
| Headphone-check result and answers to four setup questions (device type, room noise, hearing difficulty yes/no/prefer not to say, years of audio experience) | quality control, covariates | anonymous data, as above. Hearing difficulty is health-related data; the answer is optional (prefer not to say) and is used only as a covariate |
| Free-text comment (optional) | feedback | read, then deleted if it contains personal data; not published |
| Audio sample rate reported by the browser | detecting broken audio setups | anonymous data |

Not collected: name, e-mail, address, date of birth, location, IP address (the collector must not log it; see `collector/schema.sql`), cookies, analytics or advertising identifiers.
Legal basis: consent (Art. 6(1)(a) GDPR; for the optional hearing answer Art. 9(2)(a)). You may withdraw consent before submitting by closing the page; after submission, data is linked to your Prolific ID only until the ID is replaced (section 3), so withdrawal after that is no longer technically possible.
Prolific itself processes your data under its own privacy policy; I only receive what is listed above.

## 4. Who sees the data, where it is stored

Only the controller sees raw data. The collector runs on [EU-hosted server or provider: to be chosen, with a processing agreement if a third party hosts it]. No transfer outside the EU/EEA by the controller. The anonymous data set (ratings, no IDs) and the analysis code will be published with the paper.

## 5. Your rights

Access, correction, deletion, restriction, objection (while the ID is still linked), and complaint to a supervisory authority (for Julian, the data-protection authority of his German federal state: [state, to be filled in]). Contact: julian.m.kleber@gmail.com.

## 6. Consent statement shown on the page

"I am at least 18 years old, I have read the information, and I agree to take part. I know I can stop at any time."
(Implemented in `hit/hit.js`, function `consent()`; the page's short text mirrors this notice and points to the full notice in the Prolific study description.)

## 7. Ethics

No institutional review board covers an independent researcher. Risk is minimal (listening to quiet synthetic tones, no personal topics, no deception), payment is at least the German statutory minimum wage equivalent (GBP 12.50/h planned versus GBP 11.58/h floor), and no one is rejected for slow work. Participants who fail attention checks are paid unless Prolific's rejection policy applies (two or more failed attention checks in a study of five minutes or longer; see PLAN.md). Julian should decide whether to ask a peer-review body or the target journal (Acta Acustica, JCMS) whether a formal ethics statement is needed.
