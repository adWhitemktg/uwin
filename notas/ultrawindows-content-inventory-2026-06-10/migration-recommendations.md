# Migration Recommendations

These recommendations assume Sanity should hold durable business entities and generate pages from structured records where possible.

## Suggested Sanity Document Types

- `siteSettings`: business name, logo, phone, address, social URLs, consultation CTA, footer navigation.
- `service`: replacement window service overview, service benefits, warranty/installation notes.
- `serviceArea`: city/community name, state, slug, service summary, related services/materials, local proof, map/image, SEO fields.
- `windowMaterial`: aluminum, vinyl, fiberglass, composite, wood clad; benefits, constraints, gallery images, related styles.
- `windowStyle`: garden, bay/bow, double hung, single hung, picture, sliding, casement; use cases, features, images, related materials.
- `article`: editorial posts and advice content with author/date/category/related service references.
- `faq`: question, answer, topic, related service/material/style/area references.
- `testimonial`: testimonial headline, body, source/customer attribution if available, rating if available, related project/service area.
- `project`: project location, materials/styles used, gallery, outcome/proof notes, map coordinates if available.
- `offer`: financing/Synchrony offer details, terms/disclaimer fields, CTA.
- `landingPage`: curated pages that do not map cleanly to one entity, such as homepage and company/about proof pages.
- `redirectOrQuarantine`: legacy URL inventory for spam/resource pages and merge candidates.

## Suggested References Between Documents

- `serviceArea` -> references `service`, `windowMaterial`, `windowStyle`, `testimonial`, and `project` records.
- `windowMaterial` -> references compatible `windowStyle` records and shared benefit blocks.
- `windowStyle` -> references compatible `windowMaterial` records and FAQs.
- `article` -> references related `service`, `windowMaterial`, `windowStyle`, and optionally `serviceArea` records.
- `faq` -> references the topic entity it answers; render FAQ blocks on relevant pages instead of duplicating answers.
- `project` and `testimonial` -> reference `serviceArea`, `windowMaterial`, and `windowStyle` so proof can be reused across pages.
- `offer` -> referenced from homepage, service pages, and conversion sections without duplicating financing copy.

## Content That Should Become Structured Data Instead of Pages

- City/service-area coverage should be `serviceArea` records, not dozens of hand-maintained near-identical pages.
- Material availability by city should be a reference matrix, not separate pages for every material/city combination by default.
- Window styles should be structured `windowStyle` records feeding style pages, comparison blocks, and FAQs.
- FAQs should be individual `faq` records with topic references; the FAQ page can aggregate them.
- Reviews/testimonials should be structured `testimonial` records, not only headings/body blocks on one long page.
- Project map/proof should be structured `project` records or an embedded proof integration with fallback content.
- Financing should be an `offer` record reused in CTA sections.
- The `610xxxbc` resource pages should not migrate as content pages; quarantine, noindex/remove, or redirect only if they have legitimate equity.

## Migration Priorities

1. Quarantine suspicious resource pages before migrating content.
2. Normalize business facts and footer navigation in `siteSettings`.
3. Create canonical material/style/service-area records.
4. Convert location page boilerplate into templates fed by structured records and unique local proof.
5. Convert FAQs, testimonials, and project proof into reusable structured records.
