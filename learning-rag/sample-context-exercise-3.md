[Source 1: evaluate-elastic.md]
# Evaluate Elastic during a trial

Use the free 14-day {{ecloud}} trial to evaluate Elastic offerings with real data and use cases. Focus your time on the scenarios that matter most to your organization, validate key capabilities, and gather evidence to support a confident decision on whether Elastic is the right choice.

Follow this guide to complete the following:

- Define high-value use cases
- Ingest representative data
- Evaluate Elastic features against success criteria
- Measure results and document outcomes for a proof of concept (PoC)

To start your trial, go to [Sign up for a free trial](https://cloud.elastic.co/registration?page=docs&placement=docs-body).

By the end of this guide, you'll have a structured trial plan, clear evaluation results, and a solid foundation for a meaningful PoC.

## What is included in your trial

To complete each step of your evaluation, your {{ecloud}} trial provides full access to the following Elastic capabilities:

[Source 2: index.md]
# Elastic fundamentals

Welcome to Elastic fundamentals. This section helps you understand our platform, learn core concepts, and explore deployment options.

:::{tip}
If you are using a [free 14-day {{ecloud}} trial](https://cloud.elastic.co/registration?page=docs&placement=docs-body) and need guidance on building a proof of concept, refer to [Evaluate Elastic during a trial](/get-started/evaluate-elastic.md).
:::

In this section, we'll walk you through the basics of what our products offer, what they do, how they can help your business, and how to set them up. You'll get a quick look at the core features and concepts, real-world use cases, and deployment options to understand how everything fits together.

You'll also find other helpful information, such as how to use our docs, training resources, and a link to our glossary so you can familiarize yourself with our terminology.

## What is Elastic? [what-is-es]

:::{image} /get-started/images/elastic-platform.png
:alt: The Elastic platform
:::

[Source 3: evaluate-elastic.md]
vector database for building modern GenAI and semantic search applications.

To learn how {{ecloud}} works, refer to the [{{ecloud}}](/deploy-manage/deploy/elastic-cloud.md) deployment documentation.

:::{tip}
If you prefer to set up {{es}} and {{kib}} in Docker for local development or testing, refer to [](/deploy-manage/deploy/self-managed/local-development-installation-quickstart.md). By default, new installations have a Basic license that never expires. To explore all the available solutions and features, start a 30-day free trial by following the instructions in [](/deploy-manage/license/manage-your-license-in-self-managed-cluster.md).  
:::

## Trial limitations

:::{include} ../deploy-manage/deploy/_snippets/trial-limitations.md
:::

## Before you begin

A successful trial starts with clarity about what you want to achieve. Three foundational decisions shape your trial: defining your trial goal, identifying your primary use case, and choosing the deployment type that best supports it.

### Define your trial goal

To achieve the best results, clarify what success looks like for your trial.

Consider the following questions:

[Source 4: evaluate-elastic.md]
move-trial-limitations) and [Maintain access to your trial projects and data](/deploy-manage/deploy/elastic-cloud/create-an-organization.md#general-sign-up-trial-what-happens-at-the-end-of-the-trial).

::::{tip}
Depending on your organization's needs, you might want to evaluate different deployment options. Elastic offers multiple deployment types, including {{ece}} and {{eck}}. Explore the [deployment options](/deploy-manage/deploy.md) to find the best fit for your infrastructure.
::::

### Expand your implementation

After proving value with one use case:

- Consider additional solutions, such as {{observability}} + Security.
- Add data sources and integrations.
- Implement additional features such as {{ml}}, custom applications, and more.
- Onboard additional users in your organization.

### Getting help

[Source 5: evaluate-elastic.md]
ess-short}} provides the fastest path to demonstrating value. You can always explore hosted options later or migrate to production with different requirements.
:::

For detailed comparisons, refer to:

- [Deployment comparison](/deploy-manage/deploy/deployment-comparison.md): Side-by-side feature and capability comparison.
- [Differences from other {{es}} offerings](/deploy-manage/deploy/elastic-cloud/differences-from-other-elasticsearch-offerings.md): Understand how {{ecloud}} differs from self-managed deployments.

## Build your proof of concept

With your trial goal defined, follow this framework to build a PoC that demonstrates clear value and helps you make an informed decision about adopting Elastic.

### Example success criteria by use case

::::{tab-set}

:::{tab-item} Search

- Reduce time to find information by X%.
- Index and search Y documents with sub-second response times.
- Demonstrate relevance tuning for domain-specific searches.

:::

:::{tab-item} Observability

- Reduce mean time to detect (MTTD) incidents by X minutes.
- Gain visibility into application performance across Y services.
- Centralize logs from Z disparate systems.

:::

:::{tab-item} Security