---
id: answer:content-personalization:risks-caveats
concept_id: content-personalization
generated: true
artifact_level: answer
---

# What risks, caveats, or source-authority limits matter for Content And Personalization?

Avoid output caching on a Content Channel View block when its rendered content is personalized, because cached output can expose one visitor's personalized values to another visitor. Changing a localization display setting does not necessarily change the underlying processing behavior; for example, selecting a different currency symbol does not reconfigure the payment gateway. Content Component output caching can improve page speed, but it should be avoided for personalized output because a cached response can expose content intended for a different visitor. Content collections do not enforce the individual security settings of indexed items, so displaying a collection can expose restricted content to people who could not access it elsewhere in Rock.

## Top Claims

- `claim:051140ce759488e58b44`
- `claim:23bace1163888fbe0dee`
- `claim:3c0d27ef7958968d9019`
- `claim:61a34b59f2e4454facc7`

## Citations

- [Content Channel View Block](https://community.rockrms.com/documentation/digital-publishing/content-management/content-channels/content-channel-view-block)
- [Intro to Localization](https://community.rockrms.com/documentation/digital-publishing/personalization/localization/intro-to-localization)
- [Configure Content Components](https://community.rockrms.com/documentation/digital-publishing/content-management/content-component/configure-content-components)
- [Content Collection View](https://community.rockrms.com/documentation/digital-publishing/content-management/content-collections/content-collection-view)
