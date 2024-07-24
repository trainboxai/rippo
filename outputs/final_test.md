# package.json
```
{
  "name": "tailwindui-template",
  "version": "0.1.0",
  "private": true,
  "scripts": {
    "dev": "next dev",
    "build": "next build",
    "start": "next start",
    "lint": "next lint"
  },
  "browserslist": "defaults, not ie <= 11",
  "dependencies": {
    "@headlessui/react": "^1.7.13",
    "@mapbox/rehype-prism": "^0.9.0",
    "@mdx-js/loader": "^3.0.0",
    "@mdx-js/react": "^3.0.0",
    "@next/mdx": "^14.0.4",
    "@tailwindcss/typography": "^0.5.4",
    "@types/node": "^20.10.8",
    "@types/react": "^18.2.47",
    "@types/react-dom": "^18.2.18",
    "@types/webpack-env": "^1.18.1",
    "@vercel/analytics": "^1.2.2",
    "autoprefixer": "^10.4.12",
    "cheerio": "^1.0.0-rc.12",
    "clsx": "^2.1.0",
    "fast-glob": "^3.2.11",
    "feed": "^4.2.2",
    "next": "^14.0.4",
    "next-themes": "^0.2.1",
    "react": "^18.2.0",
    "react-dom": "^18.2.0",
    "remark-gfm": "^4.0.0",
    "tailwindcss": "^3.4.1",
    "typescript": "^5.3.3"
  },
  "devDependencies": {
    "eslint": "^8.56.0",
    "eslint-config-next": "^14.0.4",
    "prettier": "^3.1.1",
    "prettier-plugin-tailwindcss": "^0.5.11",
    "sharp": "0.33.1"
  }
}

```

# tailwind.config.ts
```
import typographyPlugin from '@tailwindcss/typography'
import { type Config } from 'tailwindcss'

import typographyStyles from './typography'

export default {
  content: ['./src/**/*.{js,jsx,ts,tsx}'],
  darkMode: 'selector',
  plugins: [typographyPlugin],
  theme: {
    fontSize: {
      xs: ['0.8125rem', { lineHeight: '1.5rem' }],
      sm: ['0.875rem', { lineHeight: '1.5rem' }],
      base: ['1rem', { lineHeight: '1.75rem' }],
      lg: ['1.125rem', { lineHeight: '1.75rem' }],
      xl: ['1.25rem', { lineHeight: '2rem' }],
      '2xl': ['1.5rem', { lineHeight: '2rem' }],
      '3xl': ['1.875rem', { lineHeight: '2.25rem' }],
      '4xl': ['2rem', { lineHeight: '2.5rem' }],
      '5xl': ['3rem', { lineHeight: '3.5rem' }],
      '6xl': ['3.75rem', { lineHeight: '1' }],
      '7xl': ['4.5rem', { lineHeight: '1' }],
      '8xl': ['6rem', { lineHeight: '1' }],
      '9xl': ['8rem', { lineHeight: '1' }],
    },
    typography: typographyStyles,
  },
} satisfies Config

```

# tsconfig.json
```
{
  "compilerOptions": {
    "target": "es6",
    "lib": ["dom", "dom.iterable", "esnext"],
    "allowJs": true,
    "skipLibCheck": true,
    "strict": true,
    "forceConsistentCasingInFileNames": true,
    "noEmit": true,
    "esModuleInterop": true,
    "module": "esnext",
    "moduleResolution": "bundler",
    "resolveJsonModule": true,
    "isolatedModules": true,
    "jsx": "preserve",
    "incremental": true,
    "plugins": [
      {
        "name": "next"
      }
    ],
    "paths": {
      "@/*": ["./src/*"]
    }
  },
  "include": ["next-env.d.ts", "**/*.ts", "**/*.tsx", ".next/types/**/*.ts"],
  "exclude": ["node_modules"]
}

```

# commit_push.sh
```
#!/bin/bash

if [ -z "$1" ]; then
  echo "Missing commit message"
  exit 1
fi

yarn build
git add .
git commit -m "$1"
git push origin main

```

# LICENSE.md
```
# Tailwind UI License

## Personal License

Tailwind Labs Inc. grants you an on-going, non-exclusive license to use the Components and Templates.

The license grants permission to **one individual** (the Licensee) to access and use the Components and Templates.

You **can**:

- Use the Components and Templates to create unlimited End Products.
- Modify the Components and Templates to create derivative components and templates. Those components and templates are subject to this license.
- Use the Components and Templates to create unlimited End Products for unlimited Clients.
- Use the Components and Templates to create End Products where the End Product is sold to End Users.
- Use the Components and Templates to create End Products that are open source and freely available to End Users.

You **cannot**:

- Use the Components and Templates to create End Products that are designed to allow an End User to build their own End Products using the Components and Templates or derivatives of the Components and Templates.
- Re-distribute the Components and Templates or derivatives of the Components and Templates separately from an End Product, neither in code or as design assets.
- Share your access to the Components and Templates with any other individuals.
- Use the Components and Templates to produce anything that may be deemed by Tailwind Labs Inc, in their sole and absolute discretion, to be competitive or in conflict with the business of Tailwind Labs Inc.

### Example usage

Examples of usage **allowed** by the license:

- Creating a personal website by yourself.
- Creating a website or web application for a client that will be owned by that client.
- Creating a commercial SaaS application (like an invoicing app for example) where end users have to pay a fee to use the application.
- Creating a commercial self-hosted web application that is sold to end users for a one-time fee.
- Creating a web application where the primary purpose is clearly not to simply re-distribute the components (like a conference organization app that uses the components for its UI for example) that is free and open source, where the source code is publicly available.

Examples of usage **not allowed** by the license:

- Creating a repository of your favorite Tailwind UI components or templates (or derivatives based on Tailwind UI components or templates) and publishing it publicly.
- Creating a React or Vue version of Tailwind UI and making it available either for sale or for free.
- Create a Figma or Sketch UI kit based on the Tailwind UI component designs.
- Creating a "website builder" project where end users can build their own websites using components or templates included with or derived from Tailwind UI.
- Creating a theme, template, or project starter kit using the components or templates and making it available either for sale or for free.
- Creating an admin panel tool (like [Laravel Nova](https://nova.laravel.com/) or [ActiveAdmin](https://activeadmin.info/)) that is made available either for sale or for free.

In simple terms, use Tailwind UI for anything you like as long as it doesn't compete with Tailwind UI.

### Personal License Definitions

Licensee is the individual who has purchased a Personal License.

Components and Templates are the source code and design assets made available to the Licensee after purchasing a Tailwind UI license.

End Product is any artifact produced that incorporates the Components or Templates or derivatives of the Components or Templates.

End User is a user of an End Product.

Client is an individual or entity receiving custom professional services directly from the Licensee, produced specifically for that individual or entity. Customers of software-as-a-service products are not considered clients for the purpose of this document.

## Team License

Tailwind Labs Inc. grants you an on-going, non-exclusive license to use the Components and Templates.

The license grants permission for **up to 25 Employees and Contractors of the Licensee** to access and use the Components and Templates.

You **can**:

- Use the Components and Templates to create unlimited End Products.
- Modify the Components and Templates to create derivative components and templates. Those components and templates are subject to this license.
- Use the Components and Templates to create unlimited End Products for unlimited Clients.
- Use the Components and Templates to create End Products where the End Product is sold to End Users.
- Use the Components and Templates to create End Products that are open source and freely available to End Users.

You **cannot**:

- Use the Components or Templates to create End Products that are designed to allow an End User to build their own End Products using the Components or Templates or derivatives of the Components or Templates.
- Re-distribute the Components or Templates or derivatives of the Components or Templates separately from an End Product.
- Use the Components or Templates to create End Products that are the property of any individual or entity other than the Licensee or Clients of the Licensee.
- Use the Components or Templates to produce anything that may be deemed by Tailwind Labs Inc, in their sole and absolute discretion, to be competitive or in conflict with the business of Tailwind Labs Inc.

### Example usage

Examples of usage **allowed** by the license:

- Creating a website for your company.
- Creating a website or web application for a client that will be owned by that client.
- Creating a commercial SaaS application (like an invoicing app for example) where end users have to pay a fee to use the application.
- Creating a commercial self-hosted web application that is sold to end users for a one-time fee.
- Creating a web application where the primary purpose is clearly not to simply re-distribute the components or templates (like a conference organization app that uses the components or a template for its UI for example) that is free and open source, where the source code is publicly available.

Examples of use **not allowed** by the license:

- Creating a repository of your favorite Tailwind UI components or template (or derivatives based on Tailwind UI components or templates) and publishing it publicly.
- Creating a React or Vue version of Tailwind UI and making it available either for sale or for free.
- Creating a "website builder" project where end users can build their own websites using components or templates included with or derived from Tailwind UI.
- Creating a theme or template using the components or templates and making it available either for sale or for free.
- Creating an admin panel tool (like [Laravel Nova](https://nova.laravel.com/) or [ActiveAdmin](https://activeadmin.info/)) that is made available either for sale or for free.
- Creating any End Product that is not the sole property of either your company or a client of your company. For example your employees/contractors can't use your company Tailwind UI license to build their own websites or side projects.

### Team License Definitions

Licensee is the business entity who has purchased a Team License.

Components and Templates are the source code and design assets made available to the Licensee after purchasing a Tailwind UI license.

End Product is any artifact produced that incorporates the Components or Templates or derivatives of the Components or Templates.

End User is a user of an End Product.

Employee is a full-time or part-time employee of the Licensee.

Contractor is an individual or business entity contracted to perform services for the Licensee.

Client is an individual or entity receiving custom professional services directly from the Licensee, produced specifically for that individual or entity. Customers of software-as-a-service products are not considered clients for the purpose of this document.

## Enforcement

If you are found to be in violation of the license, access to your Tailwind UI account will be terminated, and a refund may be issued at our discretion. When license violation is blatant and malicious (such as intentionally redistributing the Components or Templates through private warez channels), no refund will be issued.

The copyright of the Components and Templates is owned by Tailwind Labs Inc. You are granted only the permissions described in this license; all other rights are reserved. Tailwind Labs Inc. reserves the right to pursue legal remedies for any unauthorized use of the Components or Templates outside the scope of this license.

## Liability

Tailwind Labs Inc.’s liability to you for costs, damages, or other losses arising from your use of the Components or Templates — including third-party claims against you — is limited to a refund of your license fee. Tailwind Labs Inc. may not be held liable for any consequential damages related to your use of the Components or Templates.

This Agreement is governed by the laws of the Province of Ontario and the applicable laws of Canada. Legal proceedings related to this Agreement may only be brought in the courts of Ontario. You agree to service of process at the e-mail address on your original order.

## Questions?

Unsure which license you need, or unsure if your use case is covered by our licenses?

Email us at [support@tailwindui.com](mailto:support@tailwindui.com) with your questions.

```

# postcss.config.js
```
module.exports = {
  plugins: {
    tailwindcss: {},
    autoprefixer: {},
  },
}

```

# next.config.mjs
```
import rehypePrism from '@mapbox/rehype-prism'
import nextMDX from '@next/mdx'
import remarkGfm from 'remark-gfm'

/** @type {import('next').NextConfig} */
const nextConfig = {
  pageExtensions: ['js', 'jsx', 'ts', 'tsx', 'mdx'],
}

const withMDX = nextMDX({
  extension: /\.mdx?$/,
  options: {
    remarkPlugins: [remarkGfm],
    rehypePlugins: [rehypePrism],
  },
})

export default withMDX(nextConfig)

```

# .env
```
GEMINI_API_KEY=AIzaSyCzfarx-zwO17b5gmzQdLt--Yh7hJkW-mc
ANTHROPIC_API_KEY=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
GROQ_API_KEY=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
```

# prettier.config.js
```
/** @type {import('prettier').Options} */
module.exports = {
  singleQuote: true,
  semi: false,
  plugins: ['prettier-plugin-tailwindcss'],
}

```

# typography.ts
```
import { type PluginUtils } from 'tailwindcss/types/config'

export default function typographyStyles({ theme }: PluginUtils) {
  return {
    invert: {
      css: {
        '--tw-prose-body': 'var(--tw-prose-invert-body)',
        '--tw-prose-headings': 'var(--tw-prose-invert-headings)',
        '--tw-prose-links': 'var(--tw-prose-invert-links)',
        '--tw-prose-links-hover': 'var(--tw-prose-invert-links-hover)',
        '--tw-prose-underline': 'var(--tw-prose-invert-underline)',
        '--tw-prose-underline-hover': 'var(--tw-prose-invert-underline-hover)',
        '--tw-prose-bold': 'var(--tw-prose-invert-bold)',
        '--tw-prose-counters': 'var(--tw-prose-invert-counters)',
        '--tw-prose-bullets': 'var(--tw-prose-invert-bullets)',
        '--tw-prose-hr': 'var(--tw-prose-invert-hr)',
        '--tw-prose-quote-borders': 'var(--tw-prose-invert-quote-borders)',
        '--tw-prose-captions': 'var(--tw-prose-invert-captions)',
        '--tw-prose-code': 'var(--tw-prose-invert-code)',
        '--tw-prose-code-bg': 'var(--tw-prose-invert-code-bg)',
        '--tw-prose-pre-code': 'var(--tw-prose-invert-pre-code)',
        '--tw-prose-pre-bg': 'var(--tw-prose-invert-pre-bg)',
        '--tw-prose-pre-border': 'var(--tw-prose-invert-pre-border)',
        '--tw-prose-th-borders': 'var(--tw-prose-invert-th-borders)',
        '--tw-prose-td-borders': 'var(--tw-prose-invert-td-borders)',
      },
    },
    DEFAULT: {
      css: {
        '--tw-prose-body': theme('colors.zinc.600'),
        '--tw-prose-headings': theme('colors.zinc.900'),
        '--tw-prose-links': theme('colors.teal.500'),
        '--tw-prose-links-hover': theme('colors.teal.600'),
        '--tw-prose-underline': theme('colors.teal.500 / 0.2'),
        '--tw-prose-underline-hover': theme('colors.teal.500'),
        '--tw-prose-bold': theme('colors.zinc.900'),
        '--tw-prose-counters': theme('colors.zinc.900'),
        '--tw-prose-bullets': theme('colors.zinc.900'),
        '--tw-prose-hr': theme('colors.zinc.100'),
        '--tw-prose-quote-borders': theme('colors.zinc.200'),
        '--tw-prose-captions': theme('colors.zinc.400'),
        '--tw-prose-code': theme('colors.zinc.700'),
        '--tw-prose-code-bg': theme('colors.zinc.300 / 0.2'),
        '--tw-prose-pre-code': theme('colors.zinc.100'),
        '--tw-prose-pre-bg': theme('colors.zinc.900'),
        '--tw-prose-pre-border': 'transparent',
        '--tw-prose-th-borders': theme('colors.zinc.200'),
        '--tw-prose-td-borders': theme('colors.zinc.100'),

        '--tw-prose-invert-body': theme('colors.zinc.400'),
        '--tw-prose-invert-headings': theme('colors.zinc.200'),
        '--tw-prose-invert-links': theme('colors.teal.400'),
        '--tw-prose-invert-links-hover': theme('colors.teal.400'),
        '--tw-prose-invert-underline': theme('colors.teal.400 / 0.3'),
        '--tw-prose-invert-underline-hover': theme('colors.teal.400'),
        '--tw-prose-invert-bold': theme('colors.zinc.200'),
        '--tw-prose-invert-counters': theme('colors.zinc.200'),
        '--tw-prose-invert-bullets': theme('colors.zinc.200'),
        '--tw-prose-invert-hr': theme('colors.zinc.700 / 0.4'),
        '--tw-prose-invert-quote-borders': theme('colors.zinc.500'),
        '--tw-prose-invert-captions': theme('colors.zinc.500'),
        '--tw-prose-invert-code': theme('colors.zinc.300'),
        '--tw-prose-invert-code-bg': theme('colors.zinc.200 / 0.05'),
        '--tw-prose-invert-pre-code': theme('colors.zinc.100'),
        '--tw-prose-invert-pre-bg': 'rgb(0 0 0 / 0.4)',
        '--tw-prose-invert-pre-border': theme('colors.zinc.200 / 0.1'),
        '--tw-prose-invert-th-borders': theme('colors.zinc.700'),
        '--tw-prose-invert-td-borders': theme('colors.zinc.800'),

        // Base
        color: 'var(--tw-prose-body)',
        lineHeight: theme('lineHeight.7'),
        '> *': {
          marginTop: theme('spacing.10'),
          marginBottom: theme('spacing.10'),
        },
        p: {
          marginTop: theme('spacing.7'),
          marginBottom: theme('spacing.7'),
        },

        // Headings
        'h2, h3': {
          color: 'var(--tw-prose-headings)',
          fontWeight: theme('fontWeight.semibold'),
        },
        h2: {
          fontSize: theme('fontSize.xl')[0],
          lineHeight: theme('lineHeight.7'),
          marginTop: theme('spacing.20'),
          marginBottom: theme('spacing.4'),
        },
        h3: {
          fontSize: theme('fontSize.base')[0],
          lineHeight: theme('lineHeight.7'),
          marginTop: theme('spacing.16'),
          marginBottom: theme('spacing.4'),
        },
        ':is(h2, h3) + *': {
          marginTop: 0,
        },

        // Images
        img: {
          borderRadius: theme('borderRadius.3xl'),
        },

        // Inline elements
        a: {
          color: 'var(--tw-prose-links)',
          fontWeight: theme('fontWeight.semibold'),
          textDecoration: 'underline',
          textDecorationColor: 'var(--tw-prose-underline)',
          transitionProperty: 'color, text-decoration-color',
          transitionDuration: theme('transitionDuration.150'),
          transitionTimingFunction: theme('transitionTimingFunction.in-out'),
        },
        'a:hover': {
          color: 'var(--tw-prose-links-hover)',
          textDecorationColor: 'var(--tw-prose-underline-hover)',
        },
        strong: {
          color: 'var(--tw-prose-bold)',
          fontWeight: theme('fontWeight.semibold'),
        },
        code: {
          display: 'inline-block',
          color: 'var(--tw-prose-code)',
          fontSize: theme('fontSize.sm')[0],
          fontWeight: theme('fontWeight.semibold'),
          backgroundColor: 'var(--tw-prose-code-bg)',
          borderRadius: theme('borderRadius.lg'),
          paddingLeft: theme('spacing.1'),
          paddingRight: theme('spacing.1'),
        },
        'a code': {
          color: 'inherit',
        },
        ':is(h2, h3) code': {
          fontWeight: theme('fontWeight.bold'),
        },

        // Quotes
        blockquote: {
          paddingLeft: theme('spacing.6'),
          borderLeftWidth: theme('borderWidth.2'),
          borderLeftColor: 'var(--tw-prose-quote-borders)',
          fontStyle: 'italic',
        },

        // Figures
        figcaption: {
          color: 'var(--tw-prose-captions)',
          fontSize: theme('fontSize.sm')[0],
          lineHeight: theme('lineHeight.6'),
          marginTop: theme('spacing.3'),
        },
        'figcaption > p': {
          margin: 0,
        },

        // Lists
        ul: {
          listStyleType: 'disc',
        },
        ol: {
          listStyleType: 'decimal',
        },
        'ul, ol': {
          paddingLeft: theme('spacing.6'),
        },
        li: {
          marginTop: theme('spacing.6'),
          marginBottom: theme('spacing.6'),
          paddingLeft: theme('spacing[3.5]'),
        },
        'li::marker': {
          fontSize: theme('fontSize.sm')[0],
          fontWeight: theme('fontWeight.semibold'),
        },
        'ol > li::marker': {
          color: 'var(--tw-prose-counters)',
        },
        'ul > li::marker': {
          color: 'var(--tw-prose-bullets)',
        },
        'li :is(ol, ul)': {
          marginTop: theme('spacing.4'),
          marginBottom: theme('spacing.4'),
        },
        'li :is(li, p)': {
          marginTop: theme('spacing.3'),
          marginBottom: theme('spacing.3'),
        },

        // Code blocks
        pre: {
          color: 'var(--tw-prose-pre-code)',
          fontSize: theme('fontSize.sm')[0],
          fontWeight: theme('fontWeight.medium'),
          backgroundColor: 'var(--tw-prose-pre-bg)',
          borderRadius: theme('borderRadius.3xl'),
          padding: theme('spacing.8'),
          overflowX: 'auto',
          border: '1px solid',
          borderColor: 'var(--tw-prose-pre-border)',
        },
        'pre code': {
          display: 'inline',
          color: 'inherit',
          fontSize: 'inherit',
          fontWeight: 'inherit',
          backgroundColor: 'transparent',
          borderRadius: 0,
          padding: 0,
        },

        // Horizontal rules
        hr: {
          marginTop: theme('spacing.20'),
          marginBottom: theme('spacing.20'),
          borderTopWidth: '1px',
          borderColor: 'var(--tw-prose-hr)',
          '@screen lg': {
            marginLeft: `calc(${theme('spacing.12')} * -1)`,
            marginRight: `calc(${theme('spacing.12')} * -1)`,
          },
        },

        // Tables
        table: {
          width: '100%',
          tableLayout: 'auto',
          textAlign: 'left',
          fontSize: theme('fontSize.sm')[0],
        },
        thead: {
          borderBottomWidth: '1px',
          borderBottomColor: 'var(--tw-prose-th-borders)',
        },
        'thead th': {
          color: 'var(--tw-prose-headings)',
          fontWeight: theme('fontWeight.semibold'),
          verticalAlign: 'bottom',
          paddingBottom: theme('spacing.2'),
        },
        'thead th:not(:first-child)': {
          paddingLeft: theme('spacing.2'),
        },
        'thead th:not(:last-child)': {
          paddingRight: theme('spacing.2'),
        },
        'tbody tr': {
          borderBottomWidth: '1px',
          borderBottomColor: 'var(--tw-prose-td-borders)',
        },
        'tbody tr:last-child': {
          borderBottomWidth: 0,
        },
        'tbody td': {
          verticalAlign: 'baseline',
        },
        tfoot: {
          borderTopWidth: '1px',
          borderTopColor: 'var(--tw-prose-th-borders)',
        },
        'tfoot td': {
          verticalAlign: 'top',
        },
        ':is(tbody, tfoot) td': {
          paddingTop: theme('spacing.2'),
          paddingBottom: theme('spacing.2'),
        },
        ':is(tbody, tfoot) td:not(:first-child)': {
          paddingLeft: theme('spacing.2'),
        },
        ':is(tbody, tfoot) td:not(:last-child)': {
          paddingRight: theme('spacing.2'),
        },
      },
    },
  }
}

```

# .eslintrc.json
```
{
  "extends": "next/core-web-vitals"
}

```

# mdx-components.tsx
```
import { type MDXComponents } from 'mdx/types'
import Image, { type ImageProps } from 'next/image'

export function useMDXComponents(components: MDXComponents) {
  return {
    ...components,
    Image: (props: ImageProps) => <Image {...props} />,
  }
}

```

# src/app/not-found.tsx
```
import { Button } from '@/components/Button'
import { Container } from '@/components/Container'

export default function NotFound() {
  return (
    <Container className="flex h-full items-center pt-16 sm:pt-32">
      <div className="flex flex-col items-center">
        <p className="text-base font-semibold text-zinc-400 dark:text-zinc-500">
          404
        </p>
        <h1 className="mt-4 text-4xl font-bold tracking-tight text-zinc-800 sm:text-5xl dark:text-zinc-100">
          Page not found
        </h1>
        <p className="mt-4 text-base text-zinc-600 dark:text-zinc-400">
          Sorry, we couldn’t find the page you’re looking for.
        </p>
        <Button href="/" variant="secondary" className="mt-4">
          Go back home
        </Button>
      </div>
    </Container>
  )
}

```

# src/app/providers.tsx
```
'use client'

import { createContext, useEffect, useRef } from 'react'
import { usePathname } from 'next/navigation'
import { ThemeProvider, useTheme } from 'next-themes'

function usePrevious<T>(value: T) {
  let ref = useRef<T>()

  useEffect(() => {
    ref.current = value
  }, [value])

  return ref.current
}

function ThemeWatcher() {
  let { resolvedTheme, setTheme } = useTheme()

  useEffect(() => {
    let media = window.matchMedia('(prefers-color-scheme: dark)')

    function onMediaChange() {
      let systemTheme = media.matches ? 'dark' : 'light'
      if (resolvedTheme === systemTheme) {
        setTheme('system')
      }
    }

    onMediaChange()
    media.addEventListener('change', onMediaChange)

    return () => {
      media.removeEventListener('change', onMediaChange)
    }
  }, [resolvedTheme, setTheme])

  return null
}

export const AppContext = createContext<{ previousPathname?: string }>({})

export function Providers({ children }: { children: React.ReactNode }) {
  let pathname = usePathname()
  let previousPathname = usePrevious(pathname)

  return (
    <AppContext.Provider value={{ previousPathname }}>
      <ThemeProvider attribute="class" disableTransitionOnChange>
        <ThemeWatcher />
        {children}
      </ThemeProvider>
    </AppContext.Provider>
  )
}

```

# src/app/layout.tsx
```
import { type Metadata } from 'next'
import { Analytics } from '@vercel/analytics/react'
import { Providers } from '@/app/providers'
import { Layout } from '@/components/Layout'

import '@/styles/tailwind.css'

export const metadata: Metadata = {
  title: {
    template: '%s - Jerry Davis - Blog',
    default: 'Jerry Davis - Machine Learning Engineer',
  },
  description:
    'I am Jerry Davis, a machine learning engineer with several years of experience with vision models and more recently LLMs',
}

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="en" className="h-full antialiased" suppressHydrationWarning>
      <body className="flex h-full bg-zinc-50 dark:bg-black">
        <Providers>
          <div className="flex w-full">
            <Layout>{children}</Layout>
          </div>
        </Providers>
        <Analytics />
      </body>
    </html>
  )
}

```

# src/app/page.tsx
```
import Image, { type ImageProps } from 'next/image'
import Link from 'next/link'
import clsx from 'clsx'

import { Button } from '@/components/Button'
import { Card } from '@/components/Card'
import { Container } from '@/components/Container'
import {
  GitHubIcon,
  InstagramIcon,
  LinkedInIcon,
  XIcon,
} from '@/components/SocialIcons'
import logoAirbnb from '@/images/logos/airbnb.svg'
import logoFacebook from '@/images/logos/facebook.svg'
import logoPlanetaria from '@/images/logos/planetaria.svg'
import logoStarbucks from '@/images/logos/starbucks.svg'
import image1 from '@/images/photos/image-1.jpg'
import image2 from '@/images/photos/image-2.jpg'
import image3 from '@/images/photos/image-3.jpg'
import image4 from '@/images/photos/image-4.jpg'
import image5 from '@/images/photos/image-5.jpg'
import { type ArticleWithSlug, getAllArticles } from '@/lib/articles'
import { formatDate } from '@/lib/formatDate'

function MailIcon(props: React.ComponentPropsWithoutRef<'svg'>) {
  return (
    <svg
      viewBox="0 0 24 24"
      fill="none"
      strokeWidth="1.5"
      strokeLinecap="round"
      strokeLinejoin="round"
      aria-hidden="true"
      {...props}
    >
      <path
        d="M2.75 7.75a3 3 0 0 1 3-3h12.5a3 3 0 0 1 3 3v8.5a3 3 0 0 1-3 3H5.75a3 3 0 0 1-3-3v-8.5Z"
        className="fill-zinc-100 stroke-zinc-400 dark:fill-zinc-100/10 dark:stroke-zinc-500"
      />
      <path
        d="m4 6 6.024 5.479a2.915 2.915 0 0 0 3.952 0L20 6"
        className="stroke-zinc-400 dark:stroke-zinc-500"
      />
    </svg>
  )
}

function BriefcaseIcon(props: React.ComponentPropsWithoutRef<'svg'>) {
  return (
    <svg
      viewBox="0 0 24 24"
      fill="none"
      strokeWidth="1.5"
      strokeLinecap="round"
      strokeLinejoin="round"
      aria-hidden="true"
      {...props}
    >
      <path
        d="M2.75 9.75a3 3 0 0 1 3-3h12.5a3 3 0 0 1 3 3v8.5a3 3 0 0 1-3 3H5.75a3 3 0 0 1-3-3v-8.5Z"
        className="fill-zinc-100 stroke-zinc-400 dark:fill-zinc-100/10 dark:stroke-zinc-500"
      />
      <path
        d="M3 14.25h6.249c.484 0 .952-.002 1.316.319l.777.682a.996.996 0 0 0 1.316 0l.777-.682c.364-.32.832-.319 1.316-.319H21M8.75 6.5V4.75a2 2 0 0 1 2-2h2.5a2 2 0 0 1 2 2V6.5"
        className="stroke-zinc-400 dark:stroke-zinc-500"
      />
    </svg>
  )
}

function ArrowDownIcon(props: React.ComponentPropsWithoutRef<'svg'>) {
  return (
    <svg viewBox="0 0 16 16" fill="none" aria-hidden="true" {...props}>
      <path
        d="M4.75 8.75 8 12.25m0 0 3.25-3.5M8 12.25v-8.5"
        strokeWidth="1.5"
        strokeLinecap="round"
        strokeLinejoin="round"
      />
    </svg>
  )
}

function Article({ article }: { article: ArticleWithSlug }) {
  return (
    <Card as="article">
      <Card.Title href={`/articles/${article.slug}`}>
        {article.title}
      </Card.Title>
      <Card.Eyebrow as="time" dateTime={article.date} decorate>
        {formatDate(article.date)}
      </Card.Eyebrow>
      <Card.Description>{article.description}</Card.Description>
      <Card.Cta>Read article</Card.Cta>
    </Card>
  )
}

function SocialLink({
  icon: Icon,
  ...props
}: React.ComponentPropsWithoutRef<typeof Link> & {
  icon: React.ComponentType<{ className?: string }>
}) {
  return (
    <Link className="group -m-1 p-1" {...props}>
      <Icon className="h-6 w-6 fill-zinc-500 transition group-hover:fill-zinc-600 dark:fill-zinc-400 dark:group-hover:fill-zinc-300" />
    </Link>
  )
}

function Newsletter() {
  return (
    <form
      action="/thank-you"
      className="rounded-2xl border border-zinc-100 p-6 dark:border-zinc-700/40"
    >
      <h2 className="flex text-sm font-semibold text-zinc-900 dark:text-zinc-100">
        <MailIcon className="h-6 w-6 flex-none" />
        <span className="ml-3">Stay up to date</span>
      </h2>
      <p className="mt-2 text-sm text-zinc-600 dark:text-zinc-400">
        Get notified when I publish something new, and unsubscribe at any time.
      </p>
      <div className="mt-6 flex">
        <input
          type="email"
          placeholder="Email address"
          aria-label="Email address"
          required
          className="min-w-0 flex-auto appearance-none rounded-md border border-zinc-900/10 bg-white px-3 py-[calc(theme(spacing.2)-1px)] shadow-md shadow-zinc-800/5 placeholder:text-zinc-400 focus:border-teal-500 focus:outline-none focus:ring-4 focus:ring-teal-500/10 sm:text-sm dark:border-zinc-700 dark:bg-zinc-700/[0.15] dark:text-zinc-200 dark:placeholder:text-zinc-500 dark:focus:border-teal-400 dark:focus:ring-teal-400/10"
        />
        <Button type="submit" className="ml-4 flex-none">
          Join
        </Button>
      </div>
    </form>
  )
}

interface Role {
  company: string
  title: string
  logo: ImageProps['src']
  start: string | { label: string; dateTime: string }
  end: string | { label: string; dateTime: string }
}

function Role({ role }: { role: Role }) {
  let startLabel =
    typeof role.start === 'string' ? role.start : role.start.label
  let startDate =
    typeof role.start === 'string' ? role.start : role.start.dateTime

  let endLabel = typeof role.end === 'string' ? role.end : role.end.label
  let endDate = typeof role.end === 'string' ? role.end : role.end.dateTime

  return (
    <li className="flex gap-4">
      <div className="relative mt-1 flex h-10 w-10 flex-none items-center justify-center rounded-full shadow-md shadow-zinc-800/5 ring-1 ring-zinc-900/5 dark:border dark:border-zinc-700/50 dark:bg-zinc-800 dark:ring-0">
        <Image src={role.logo} alt="" className="h-7 w-7" unoptimized />
      </div>
      <dl className="flex flex-auto flex-wrap gap-x-2">
        <dt className="sr-only">Company</dt>
        <dd className="w-full flex-none text-sm font-medium text-zinc-900 dark:text-zinc-100">
          {role.company}
        </dd>
        <dt className="sr-only">Role</dt>
        <dd className="text-xs text-zinc-500 dark:text-zinc-400">
          {role.title}
        </dd>
        <dt className="sr-only">Date</dt>
        <dd
          className="ml-auto text-xs text-zinc-400 dark:text-zinc-500"
          aria-label={`${startLabel} until ${endLabel}`}
        >
          <time dateTime={startDate}>{startLabel}</time>{' '}
          <span aria-hidden="true">—</span>{' '}
          <time dateTime={endDate}>{endLabel}</time>
        </dd>
      </dl>
    </li>
  )
}

function Resume() {
  let resume: Array<Role> = [
    {
      company: 'Planetaria',
      title: 'CEO',
      logo: logoPlanetaria,
      start: '2019',
      end: {
        label: 'Present',
        dateTime: new Date().getFullYear().toString(),
      },
    },
    {
      company: 'Airbnb',
      title: 'Product Designer',
      logo: logoAirbnb,
      start: '2014',
      end: '2019',
    },
    {
      company: 'Facebook',
      title: 'iOS Software Engineer',
      logo: logoFacebook,
      start: '2011',
      end: '2014',
    },
    {
      company: 'Starbucks',
      title: 'Shift Supervisor',
      logo: logoStarbucks,
      start: '2008',
      end: '2011',
    },
  ]

  return (
    <div className="rounded-2xl border border-zinc-100 p-6 dark:border-zinc-700/40">
      <h2 className="flex text-sm font-semibold text-zinc-900 dark:text-zinc-100">
        <BriefcaseIcon className="h-6 w-6 flex-none" />
        <span className="ml-3">Work</span>
      </h2>
      <ol className="mt-6 space-y-4">
        {resume.map((role, roleIndex) => (
          <Role key={roleIndex} role={role} />
        ))}
      </ol>
      <Button href="#" variant="secondary" className="group mt-6 w-full">
        Download CV
        <ArrowDownIcon className="h-4 w-4 stroke-zinc-400 transition group-active:stroke-zinc-600 dark:group-hover:stroke-zinc-50 dark:group-active:stroke-zinc-50" />
      </Button>
    </div>
  )
}

function Photos() {
  let rotations = ['rotate-2', '-rotate-2', 'rotate-2', 'rotate-2', '-rotate-2']

  return (
    <div className="mt-16 sm:mt-20">
      <div className="-my-4 flex justify-center gap-5 overflow-hidden py-4 sm:gap-8">
        {[image1, image2, image3, image4, image5].map((image, imageIndex) => (
          <div
            key={image.src}
            className={clsx(
              'relative aspect-[9/10] w-44 flex-none overflow-hidden rounded-xl bg-zinc-100 sm:w-72 sm:rounded-2xl dark:bg-zinc-800',
              rotations[imageIndex % rotations.length],
            )}
          >
            <Image
              src={image}
              alt=""
              sizes="(min-width: 640px) 18rem, 11rem"
              className="absolute inset-0 h-full w-full object-cover"
            />
          </div>
        ))}
      </div>
    </div>
  )
}

export default async function Home() {
  let articles = (await getAllArticles()).slice(0, 4)

  return (
    <>
      <Container className="mt-9">
        <div className="max-w-2xl">
          <h1 className="text-4xl font-bold tracking-tight text-zinc-800 sm:text-5xl dark:text-zinc-100">
            ML Engineer | LLMs, Computer Vision | Tinkerer
          </h1>
          <p className="mt-6 text-base text-zinc-600 dark:text-zinc-400">
            I am Jerry Davis, a machine learning engineer with several years of
            experience with vision models and more recently LLMs (Large Language
            Models). I have contributed to projects across many industries
            (Pharmaceutical, Insurance, Manufacturing, Sports, Banking &
            Finance). I enjoy tinkering with technology.
          </p>
          <div className="mt-6 flex gap-6">
            <SocialLink
              href="https://twitter.com/JerryDavis888"
              aria-label="Follow on X"
              icon={XIcon}
            />

            <SocialLink
              href="https://github.com/jerrydav1s"
              aria-label="Follow on GitHub"
              icon={GitHubIcon}
            />
            <SocialLink
              href="https://www.linkedin.com/in/jerry-davis-b76148269"
              aria-label="Follow on LinkedIn"
              icon={LinkedInIcon}
            />
          </div>
        </div>
      </Container>

      <Container className="mt-24 md:mt-28">
        <div className="mx-auto grid max-w-xl grid-cols-1 gap-y-20 lg:max-w-none lg:grid-cols-2">
          <div className="flex flex-col gap-16">
            {articles.map((article) => (
              <Article key={article.slug} article={article} />
            ))}
          </div>
          <div className="space-y-10 lg:pl-16 xl:pl-24"></div>
        </div>
      </Container>
    </>
  )
}

```

# src/app/projects/page.tsx
```
import { type Metadata } from 'next'
import Image from 'next/image'

import { Card } from '@/components/Card'
import { SimpleLayout } from '@/components/SimpleLayout'
import logoAnimaginary from '@/images/logos/animaginary.svg'
import logoCosmos from '@/images/logos/cosmos.svg'
import logoHelioStream from '@/images/logos/helio-stream.svg'
import logoOpenShuttle from '@/images/logos/open-shuttle.svg'
import logoPlanetaria from '@/images/logos/planetaria.svg'

const projects = [
  {
    name: 'Planetaria',
    description:
      'Creating technology to empower civilians to explore space on their own terms.',
    link: { href: 'http://planetaria.tech', label: 'planetaria.tech' },
    logo: logoPlanetaria,
  },
  {
    name: 'Animaginary',
    description:
      'High performance web animation library, hand-written in optimized WASM.',
    link: { href: '#', label: 'github.com' },
    logo: logoAnimaginary,
  },
  {
    name: 'HelioStream',
    description:
      'Real-time video streaming library, optimized for interstellar transmission.',
    link: { href: '#', label: 'github.com' },
    logo: logoHelioStream,
  },
  {
    name: 'cosmOS',
    description:
      'The operating system that powers our Planetaria space shuttles.',
    link: { href: '#', label: 'github.com' },
    logo: logoCosmos,
  },
  {
    name: 'OpenShuttle',
    description:
      'The schematics for the first rocket I designed that successfully made it to orbit.',
    link: { href: '#', label: 'github.com' },
    logo: logoOpenShuttle,
  },
]

function LinkIcon(props: React.ComponentPropsWithoutRef<'svg'>) {
  return (
    <svg viewBox="0 0 24 24" aria-hidden="true" {...props}>
      <path
        d="M15.712 11.823a.75.75 0 1 0 1.06 1.06l-1.06-1.06Zm-4.95 1.768a.75.75 0 0 0 1.06-1.06l-1.06 1.06Zm-2.475-1.414a.75.75 0 1 0-1.06-1.06l1.06 1.06Zm4.95-1.768a.75.75 0 1 0-1.06 1.06l1.06-1.06Zm3.359.53-.884.884 1.06 1.06.885-.883-1.061-1.06Zm-4.95-2.12 1.414-1.415L12 6.344l-1.415 1.413 1.061 1.061Zm0 3.535a2.5 2.5 0 0 1 0-3.536l-1.06-1.06a4 4 0 0 0 0 5.656l1.06-1.06Zm4.95-4.95a2.5 2.5 0 0 1 0 3.535L17.656 12a4 4 0 0 0 0-5.657l-1.06 1.06Zm1.06-1.06a4 4 0 0 0-5.656 0l1.06 1.06a2.5 2.5 0 0 1 3.536 0l1.06-1.06Zm-7.07 7.07.176.177 1.06-1.06-.176-.177-1.06 1.06Zm-3.183-.353.884-.884-1.06-1.06-.884.883 1.06 1.06Zm4.95 2.121-1.414 1.414 1.06 1.06 1.415-1.413-1.06-1.061Zm0-3.536a2.5 2.5 0 0 1 0 3.536l1.06 1.06a4 4 0 0 0 0-5.656l-1.06 1.06Zm-4.95 4.95a2.5 2.5 0 0 1 0-3.535L6.344 12a4 4 0 0 0 0 5.656l1.06-1.06Zm-1.06 1.06a4 4 0 0 0 5.657 0l-1.061-1.06a2.5 2.5 0 0 1-3.535 0l-1.061 1.06Zm7.07-7.07-.176-.177-1.06 1.06.176.178 1.06-1.061Z"
        fill="currentColor"
      />
    </svg>
  )
}

export const metadata: Metadata = {
  title: 'Projects',
  description: 'Things I’ve made trying to put my dent in the universe.',
}

export default function Projects() {
  return (
    <SimpleLayout
      title="Things I’ve made trying to put my dent in the universe."
      intro="I’ve worked on tons of little projects over the years but these are the ones that I’m most proud of. Many of them are open-source, so if you see something that piques your interest, check out the code and contribute if you have ideas for how it can be improved."
    >
      <ul
        role="list"
        className="grid grid-cols-1 gap-x-12 gap-y-16 sm:grid-cols-2 lg:grid-cols-3"
      >
        {projects.map((project) => (
          <Card as="li" key={project.name}>
            <div className="relative z-10 flex h-12 w-12 items-center justify-center rounded-full bg-white shadow-md shadow-zinc-800/5 ring-1 ring-zinc-900/5 dark:border dark:border-zinc-700/50 dark:bg-zinc-800 dark:ring-0">
              <Image
                src={project.logo}
                alt=""
                className="h-8 w-8"
                unoptimized
              />
            </div>
            <h2 className="mt-6 text-base font-semibold text-zinc-800 dark:text-zinc-100">
              <Card.Link href={project.link.href}>{project.name}</Card.Link>
            </h2>
            <Card.Description>{project.description}</Card.Description>
            <p className="relative z-10 mt-6 flex text-sm font-medium text-zinc-400 transition group-hover:text-teal-500 dark:text-zinc-200">
              <LinkIcon className="h-6 w-6 flex-none" />
              <span className="ml-2">{project.link.label}</span>
            </p>
          </Card>
        ))}
      </ul>
    </SimpleLayout>
  )
}

```

# src/app/videos/page.tsx
```
import { type Metadata } from 'next'

import { Card } from '@/components/Card'
import { Section } from '@/components/Section'
import { SimpleLayout } from '@/components/SimpleLayout'

function SpeakingSection({
  children,
  ...props
}: React.ComponentPropsWithoutRef<typeof Section>) {
  return (
    <Section {...props}>
      <div className="space-y-16">{children}</div>
    </Section>
  )
}

function Appearance({
  title,
  description,
  event,
  cta,
  href,
}: {
  title: string
  description: string
  event: string
  cta: string
  href: string
}) {
  return (
    <Card as="article">
      <Card.Title as="h3" href={href}>
        {title}
      </Card.Title>
      <Card.Eyebrow decorate>{event}</Card.Eyebrow>
      <Card.Description>{description}</Card.Description>
      <Card.Cta>{cta}</Card.Cta>
    </Card>
  )
}

export const metadata: Metadata = {
  title: 'Videos',
  description: 'Watch my videos YouTube.',
}

export default function Speaking() {
  return (
    <SimpleLayout
      title="Have a look at my YouTube channel. "
      intro="One of my favorite ways to share my ideas is by making video content. It is another dimension and gives me the opportunity to express my ideas."
    >
      <div className="space-y-20">
        <SpeakingSection title="How-to-guides">
          <Appearance
            href="https://www.youtube.com/watch?v=WJbIdsoDWD4"
            title="Deploying and infer Hugging Face Model on Amazon SageMaker"
            description="This tutorial will guide you through the process of deploying a Hugging Face model to Amazon SageMaker."
            event="HugginFace"
            cta="Watch video"
          />
          <Appearance
            href="#"
            title="How to fine-tune an open source model on your Macbook with MLX"
            description="In the oven cooking . . ."
            event="MLX"
            cta="Watch video"
          />
        </SpeakingSection>
        <SpeakingSection title="Reviews and explainers">
          <Appearance
            href="#"
            title="Key structures of a Large Language Model"
            description="In the oven cooking . . ."
            event="Large Language Models"
            cta="Watch now"
          />
          <Appearance
            href="#"
            title="Shop traffic analysis with computer vision"
            description="In the oven cooking . . ."
            event="The Escape Velocity Show, March 2022"
            cta="Watch now"
          />
        </SpeakingSection>
      </div>
    </SimpleLayout>
  )
}

```

# src/app/about/page.tsx
```
import { type Metadata } from 'next'
import Image from 'next/image'
import Link from 'next/link'
import clsx from 'clsx'

import { Container } from '@/components/Container'
import {
  GitHubIcon,
  InstagramIcon,
  LinkedInIcon,
  XIcon,
} from '@/components/SocialIcons'
import portraitImage from '@/images/portrait.jpg'

function SocialLink({
  className,
  href,
  children,
  icon: Icon,
}: {
  className?: string
  href: string
  icon: React.ComponentType<{ className?: string }>
  children: React.ReactNode
}) {
  return (
    <li className={clsx(className, 'flex')}>
      <Link
        href={href}
        className="group flex text-sm font-medium text-zinc-800 transition hover:text-teal-500 dark:text-zinc-200 dark:hover:text-teal-500"
      >
        <Icon className="h-6 w-6 flex-none fill-zinc-500 transition group-hover:fill-teal-500" />
        <span className="ml-4">{children}</span>
      </Link>
    </li>
  )
}

function MailIcon(props: React.ComponentPropsWithoutRef<'svg'>) {
  return (
    <svg viewBox="0 0 24 24" aria-hidden="true" {...props}>
      <path
        fillRule="evenodd"
        d="M6 5a3 3 0 0 0-3 3v8a3 3 0 0 0 3 3h12a3 3 0 0 0 3-3V8a3 3 0 0 0-3-3H6Zm.245 2.187a.75.75 0 0 0-.99 1.126l6.25 5.5a.75.75 0 0 0 .99 0l6.25-5.5a.75.75 0 0 0-.99-1.126L12 12.251 6.245 7.187Z"
      />
    </svg>
  )
}

export const metadata: Metadata = {
  title: 'About',
  description:
    'I’m Spencer Sharp. I live in New York City, where I design the future.',
}

export default function About() {
  return (
    <Container className="mt-16 sm:mt-32">
      <div className="grid grid-cols-1 gap-y-16 lg:grid-cols-2 lg:grid-rows-[auto_1fr] lg:gap-y-12">
        <div className="lg:pl-20">
          <div className="max-w-xs px-2.5 lg:max-w-none">
            <Image
              src={portraitImage}
              alt=""
              sizes="(min-width: 1024px) 32rem, 20rem"
              className="aspect-square rotate-3 rounded-2xl bg-zinc-100 object-cover dark:bg-zinc-800"
            />
          </div>
        </div>
        <div className="lg:order-first lg:row-span-2">
          <h1 className="text-4xl font-bold tracking-tight text-zinc-800 sm:text-5xl dark:text-zinc-100">
            I’m Spencer Sharp. I live in New York City, where I design the
            future.
          </h1>
          <div className="mt-6 space-y-7 text-base text-zinc-600 dark:text-zinc-400">
            <p>
              I’ve loved making things for as long as I can remember, and wrote
              my first program when I was 6 years old, just two weeks after my
              mom brought home the brand new Macintosh LC 550 that I taught
              myself to type on.
            </p>
            <p>
              The only thing I loved more than computers as a kid was space.
              When I was 8, I climbed the 40-foot oak tree at the back of our
              yard while wearing my older sister’s motorcycle helmet, counted
              down from three, and jumped — hoping the tree was tall enough that
              with just a bit of momentum I’d be able to get to orbit.
            </p>
            <p>
              I spent the next few summers indoors working on a rocket design,
              while I recovered from the multiple surgeries it took to fix my
              badly broken legs. It took nine iterations, but when I was 15 I
              sent my dad’s Blackberry into orbit and was able to transmit a
              photo back down to our family computer from space.
            </p>
            <p>
              Today, I’m the founder of Planetaria, where we’re working on
              civilian space suits and manned shuttle kits you can assemble at
              home so that the next generation of kids really <em>can</em> make
              it to orbit — from the comfort of their own backyards.
            </p>
          </div>
        </div>
        <div className="lg:pl-20">
          <ul role="list">
            <SocialLink href="#" icon={XIcon}>
              Follow on X
            </SocialLink>
            <SocialLink href="#" icon={InstagramIcon} className="mt-4">
              Follow on Instagram
            </SocialLink>
            <SocialLink href="#" icon={GitHubIcon} className="mt-4">
              Follow on GitHub
            </SocialLink>
            <SocialLink href="#" icon={LinkedInIcon} className="mt-4">
              Follow on LinkedIn
            </SocialLink>
            <SocialLink
              href="mailto:spencer@planetaria.tech"
              icon={MailIcon}
              className="mt-8 border-t border-zinc-100 pt-8 dark:border-zinc-700/40"
            >
              spencer@planetaria.tech
            </SocialLink>
          </ul>
        </div>
      </div>
    </Container>
  )
}

```

# src/app/thank-you/page.tsx
```
import { type Metadata } from 'next'

import { SimpleLayout } from '@/components/SimpleLayout'

export const metadata: Metadata = {
  title: 'You’re subscribed',
  description: 'Thanks for subscribing to my newsletter.',
}

export default function ThankYou() {
  return (
    <SimpleLayout
      title="Thanks for subscribing."
      intro="I’ll send you an email any time I publish a new blog post, release a new project, or have anything interesting to share that I think you’d want to hear about. You can unsubscribe at any time, no hard feelings."
    />
  )
}

```

# src/app/articles/page.tsx
```
import { type Metadata } from 'next'

import { Card } from '@/components/Card'
import { SimpleLayout } from '@/components/SimpleLayout'
import { type ArticleWithSlug, getAllArticles } from '@/lib/articles'
import { formatDate } from '@/lib/formatDate'

function Article({ article }: { article: ArticleWithSlug }) {
  return (
    <article className="md:grid md:grid-cols-4 md:items-baseline">
      <Card className="md:col-span-3">
        <Card.Title href={`/articles/${article.slug}`}>
          {article.title}
        </Card.Title>
        <Card.Eyebrow
          as="time"
          dateTime={article.date}
          className="md:hidden"
          decorate
        >
          {formatDate(article.date)}
        </Card.Eyebrow>
        <Card.Description>{article.description}</Card.Description>
        <Card.Cta>Read article</Card.Cta>
      </Card>
      <Card.Eyebrow
        as="time"
        dateTime={article.date}
        className="mt-1 hidden md:block"
      >
        {formatDate(article.date)}
      </Card.Eyebrow>
    </article>
  )
}

export const metadata: Metadata = {
  title: 'Articles',
  description:
    'All of my long-form thoughts on programming, leadership, product design, and more, collected in chronological order.',
}

export default async function ArticlesIndex() {
  let articles = await getAllArticles()

  return (
    <SimpleLayout
      title="I post things I find interesting or useful to me and hopefully to others"
      intro="All of my thoughts on machine learning, software development, latest news, and more, collected in chronological order."
    >
      <div className="md:border-l md:border-zinc-100 md:pl-6 md:dark:border-zinc-700/40">
        <div className="flex max-w-3xl flex-col space-y-16">
          {articles.map((article) => (
            <Article key={article.slug} article={article} />
          ))}
        </div>
      </div>
    </SimpleLayout>
  )
}

```

# src/app/articles/how-to-login-to-github-from-a-linux-machine/page.mdx
```
import { ArticleLayout } from '@/components/ArticleLayout'

export const article = {
  author: 'Jerry Davis',
  date: '2023-04-12',
  title: 'How to Login to GitHub from a Linux Machine: A Step-by-Step Guide',
  description:
    'Follow these simple steps to set up your Linux machine for collaborating on GitHub repositories. Learn how to install Git, configure your account, generate an SSH key, and connect to GitHub seamlessly.',
}

export const metadata = {
  title: article.title,
  description: article.description,
}

export default (props) => <ArticleLayout article={article} {...props} />

Are you setting up your Linux machine to collaborate on GitHub repositories? Follow these simple steps to login to GitHub and start pushing and pulling code with ease.

1. **Install Git**: If Git isn't already installed on your Linux machine, you can install it using your package manager. For example, on Ubuntu, you can run:

   ```bash
   sudo apt install git
   ```

2. **Configure Git**: Set up your Git username and email by running the following commands, replacing "Your GitHub Username" and "Your GitHub Email" with your actual GitHub username and email:

   ```bash
   git config --global user.name "Your GitHub Username"
   git config --global user.email "Your GitHub Email"
   ```

3. **Generate SSH Key**: Generate a new SSH key using the following command. Make sure to replace "your_email@example.com" with the email associated with your GitHub account.

   ```bash
   ssh-keygen -t rsa -b 4096 -C "your_email@example.com"
   ```

4. **Add SSH Key to SSH Agent**: Add your SSH key to the SSH agent to manage your SSH keys easily.

   ```bash
   eval "$(ssh-agent -s)"
   ssh-add ~/.ssh/id_rsa
   ```

5. **Copy SSH Key to Clipboard**: Install xclip if not already installed and copy your SSH key to the clipboard.

   ```bash
   sudo apt-get install xclip
   xclip -sel clip < ~/.ssh/id_rsa.pub
   ```

6. **Add SSH Key to GitHub**: Go to your GitHub account settings, navigate to "SSH and GPG keys," and click on "New SSH key" or "Add SSH key." Paste your SSH key into the "Key" field and add a descriptive title. Click "Add SSH key" to save.

7. **Test SSH Connection**: Ensure your SSH connection to GitHub is successful by running the following command:

   ```bash
   ssh -T git@github.com
   ```

That's it! You're now ready to collaborate on GitHub repositories from your Linux machine. Happy coding!

```

# src/app/articles/deploying-a-hugging-face-model-to-amazon-sagemaker/page.mdx
```
import { ArticleLayout } from '@/components/ArticleLayout'

export const article = {
  author: 'Jerry Davis',
  date: '2024-04-18',
  title: 'Deploying a Hugging Face Model to Amazon SageMaker',
  description:
    'This tutorial will guide you through the process of deploying a Hugging Face model to Amazon SageMaker. By following these steps, you will be able to host your model on a scalable and reliable platform.',
}

export const metadata = {
  title: article.title,
  description: article.description,
}

export default (props) => <ArticleLayout article={article} {...props} />

# Deploying a Hugging Face Model to Amazon SageMaker

This tutorial will guide you through the process of deploying a Hugging Face model to Amazon SageMaker. By following these steps, you'll be able to host your model on a scalable and reliable platform.

## Prerequisites

Before getting started, make sure you have the following:

1. Create a SageMaker domain in the AWS Console.
2. Create an IAM account with SageMaker admin access and generate an access key.
3. Create an IAM role with SageMaker admin access.

## Setup

### Install AWS CLI

Install the AWS Command Line Interface (CLI) on your local machine. You can follow the official AWS documentation for installation instructions specific to your operating system.

### Configure AWS CLI

Run the following command in your terminal:

```
aws configure
```

Enter the access key created earlier and specify your AWS region when prompted.

## Deployment

1. Go to the Hugging Face website and find the model you want to deploy.
2. Click on the deploy button and copy the template code provided.
3. Open Visual Studio Code (VSCode) and create a new file.
4. Paste the template code from Hugging Face into the file.
5. Modify the role name in the code to match the IAM role you created earlier:

```python
role = iam.get_role(RoleName='YOUR_ROLE_NAME_HERE')['Role']['Arn']
```

6. Save the file as `sagemaker_deploy.py`.
7. Run the `sagemaker_deploy.py` script to deploy your model to SageMaker.

## Verification

1. Open the SageMaker console in the AWS Management Console.
2. Verify that the model has been successfully deployed and the endpoint is active.

## Inference

1. Create a new file in VSCode and name it `sagemaker_infer.py`.
2. Write your inference code in the `sagemaker_infer.py` file to make predictions using the deployed model.
3. Run the `sagemaker_infer.py` script to perform inference.

Congratulations! You have successfully deployed a Hugging Face model to Amazon SageMaker. Feel free to explore and experiment with your deployed model.

## Additional Resources

- [AWS CLI Documentation](https://aws.amazon.com/cli/)
- [Amazon SageMaker Documentation](https://docs.aws.amazon.com/sagemaker/)
- [Hugging Face Documentation](https://huggingface.co/docs/)

If you have any questions or need some guidance on how to do this at scale please get in touch.
Happy deploying and have fun!

```

# src/app/uses/page.tsx
```
import { Card } from '@/components/Card'
import { Section } from '@/components/Section'
import { SimpleLayout } from '@/components/SimpleLayout'

function ToolsSection({
  children,
  ...props
}: React.ComponentPropsWithoutRef<typeof Section>) {
  return (
    <Section {...props}>
      <ul role="list" className="space-y-16">
        {children}
      </ul>
    </Section>
  )
}

function Tool({
  title,
  href,
  children,
}: {
  title: string
  href?: string
  children: React.ReactNode
}) {
  return (
    <Card as="li">
      <Card.Title as="h3" href={href}>
        {title}
      </Card.Title>
      <Card.Description>{children}</Card.Description>
    </Card>
  )
}

export const metadata = {
  title: 'Uses',
  description: 'Software I use, gadgets I love, and other things I recommend.',
}

export default function Uses() {
  return (
    <SimpleLayout
      title="Software I use, gadgets I love, and other things I recommend."
      intro="I get asked a lot about the things I use to build software, stay productive, or buy to fool myself into thinking I’m being productive when I’m really just procrastinating. Here’s a big list of all of my favorite stuff."
    >
      <div className="space-y-20">
        <ToolsSection title="Workstation">
          <Tool title="16” MacBook Pro, M1 Max, 64GB RAM (2021)">
            I was using an Intel-based 16” MacBook Pro prior to this and the
            difference is night and day. I’ve never heard the fans turn on a
            single time, even under the incredibly heavy loads I put it through
            with our various launch simulations.
          </Tool>
          <Tool title="Apple Pro Display XDR (Standard Glass)">
            The only display on the market if you want something HiDPI and
            bigger than 27”. When you’re working at planetary scale, every pixel
            you can get counts.
          </Tool>
          <Tool title="IBM Model M SSK Industrial Keyboard">
            They don’t make keyboards the way they used to. I buy these any time
            I see them go up for sale and keep them in storage in case I need
            parts or need to retire my main.
          </Tool>
          <Tool title="Apple Magic Trackpad">
            Something about all the gestures makes me feel like a wizard with
            special powers. I really like feeling like a wizard with special
            powers.
          </Tool>
          <Tool title="Herman Miller Aeron Chair">
            If I’m going to slouch in the worst ergonomic position imaginable
            all day, I might as well do it in an expensive chair.
          </Tool>
        </ToolsSection>
        <ToolsSection title="Development tools">
          <Tool title="Sublime Text 4">
            I don’t care if it’s missing all of the fancy IDE features everyone
            else relies on, Sublime Text is still the best text editor ever
            made.
          </Tool>
          <Tool title="iTerm2">
            I’m honestly not even sure what features I get with this that aren’t
            just part of the macOS Terminal but it’s what I use.
          </Tool>
          <Tool title="TablePlus">
            Great software for working with databases. Has saved me from
            building about a thousand admin interfaces for my various projects
            over the years.
          </Tool>
        </ToolsSection>
        <ToolsSection title="Design">
          <Tool title="Figma">
            We started using Figma as just a design tool but now it’s become our
            virtual whiteboard for the entire company. Never would have expected
            the collaboration features to be the real hook.
          </Tool>
        </ToolsSection>
        <ToolsSection title="Productivity">
          <Tool title="Alfred">
            It’s not the newest kid on the block but it’s still the fastest. The
            Sublime Text of the application launcher world.
          </Tool>
          <Tool title="Reflect">
            Using a daily notes system instead of trying to keep things
            organized by topics has been super powerful for me. And with
            Reflect, it’s still easy for me to keep all of that stuff
            discoverable by topic even though all of my writing happens in the
            daily note.
          </Tool>
          <Tool title="SavvyCal">
            Great tool for scheduling meetings while protecting my calendar and
            making sure I still have lots of time for deep work during the week.
          </Tool>
          <Tool title="Focus">
            Simple tool for blocking distracting websites when I need to just do
            the work and get some momentum going.
          </Tool>
        </ToolsSection>
      </div>
    </SimpleLayout>
  )
}

```

# src/styles/tailwind.css
```
@import 'tailwindcss/base';
@import 'tailwindcss/components';
@import './prism.css';
@import 'tailwindcss/utilities';

```

# src/styles/prism.css
```
pre[class*='language-'] {
  color: theme('colors.zinc.100');
}

.token.tag,
.token.class-name,
.token.selector,
.token.selector .class,
.token.selector.class,
.token.function {
  color: theme('colors.pink.400');
}

.token.attr-name,
.token.keyword,
.token.rule,
.token.pseudo-class,
.token.important {
  color: theme('colors.zinc.300');
}

.token.module {
  color: theme('colors.pink.400');
}

.token.attr-value,
.token.class,
.token.string,
.token.property {
  color: theme('colors.teal.300');
}

.token.punctuation,
.token.attr-equals {
  color: theme('colors.zinc.500');
}

.token.unit,
.language-css .token.function {
  color: theme('colors.sky.200');
}

.token.comment,
.token.operator,
.token.combinator {
  color: theme('colors.zinc.400');
}

```

# src/lib/formatDate.ts
```
export function formatDate(dateString: string) {
  return new Date(`${dateString}T00:00:00Z`).toLocaleDateString('en-US', {
    day: 'numeric',
    month: 'long',
    year: 'numeric',
    timeZone: 'UTC',
  })
}

```

# src/lib/articles.ts
```
import glob from 'fast-glob'

interface Article {
  title: string
  description: string
  author: string
  date: string
}

export interface ArticleWithSlug extends Article {
  slug: string
}

async function importArticle(
  articleFilename: string,
): Promise<ArticleWithSlug> {
  let { article } = (await import(`../app/articles/${articleFilename}`)) as {
    default: React.ComponentType
    article: Article
  }

  return {
    slug: articleFilename.replace(/(\/page)?\.mdx$/, ''),
    ...article,
  }
}

export async function getAllArticles() {
  let articleFilenames = await glob('*/page.mdx', {
    cwd: './src/app/articles',
  })

  let articles = await Promise.all(articleFilenames.map(importArticle))

  return articles.sort((a, z) => +new Date(z.date) - +new Date(a.date))
}

```

# src/components/SimpleLayout.tsx
```
import { Container } from '@/components/Container'

export function SimpleLayout({
  title,
  intro,
  children,
}: {
  title: string
  intro: string
  children?: React.ReactNode
}) {
  return (
    <Container className="mt-16 sm:mt-32">
      <header className="max-w-2xl">
        <h1 className="text-4xl font-bold tracking-tight text-zinc-800 sm:text-5xl dark:text-zinc-100">
          {title}
        </h1>
        <p className="mt-6 text-base text-zinc-600 dark:text-zinc-400">
          {intro}
        </p>
      </header>
      {children && <div className="mt-16 sm:mt-20">{children}</div>}
    </Container>
  )
}

```

# src/components/Section.tsx
```
import { useId } from 'react'

export function Section({
  title,
  children,
}: {
  title: string
  children: React.ReactNode
}) {
  let id = useId()

  return (
    <section
      aria-labelledby={id}
      className="md:border-l md:border-zinc-100 md:pl-6 md:dark:border-zinc-700/40"
    >
      <div className="grid max-w-3xl grid-cols-1 items-baseline gap-y-8 md:grid-cols-4">
        <h2
          id={id}
          className="text-sm font-semibold text-zinc-800 dark:text-zinc-100"
        >
          {title}
        </h2>
        <div className="md:col-span-3">{children}</div>
      </div>
    </section>
  )
}

```

# src/components/Layout.tsx
```
import { Footer } from '@/components/Footer'
import { Header } from '@/components/Header'

export function Layout({ children }: { children: React.ReactNode }) {
  return (
    <>
      <div className="fixed inset-0 flex justify-center sm:px-8">
        <div className="flex w-full max-w-7xl lg:px-8">
          <div className="w-full bg-white ring-1 ring-zinc-100 dark:bg-zinc-900 dark:ring-zinc-300/20" />
        </div>
      </div>
      <div className="relative flex w-full flex-col">
        <Header />
        <main className="flex-auto">{children}</main>
        <Footer />
      </div>
    </>
  )
}

```

# src/components/Prose.tsx
```
import clsx from 'clsx'

export function Prose({
  className,
  ...props
}: React.ComponentPropsWithoutRef<'div'>) {
  return (
    <div className={clsx(className, 'prose dark:prose-invert')} {...props} />
  )
}

```

# src/components/Container.tsx
```
import { forwardRef } from 'react'
import clsx from 'clsx'

export const ContainerOuter = forwardRef<
  React.ElementRef<'div'>,
  React.ComponentPropsWithoutRef<'div'>
>(function OuterContainer({ className, children, ...props }, ref) {
  return (
    <div ref={ref} className={clsx('sm:px-8', className)} {...props}>
      <div className="mx-auto w-full max-w-7xl lg:px-8">{children}</div>
    </div>
  )
})

export const ContainerInner = forwardRef<
  React.ElementRef<'div'>,
  React.ComponentPropsWithoutRef<'div'>
>(function InnerContainer({ className, children, ...props }, ref) {
  return (
    <div
      ref={ref}
      className={clsx('relative px-4 sm:px-8 lg:px-12', className)}
      {...props}
    >
      <div className="mx-auto max-w-2xl lg:max-w-5xl">{children}</div>
    </div>
  )
})

export const Container = forwardRef<
  React.ElementRef<typeof ContainerOuter>,
  React.ComponentPropsWithoutRef<typeof ContainerOuter>
>(function Container({ children, ...props }, ref) {
  return (
    <ContainerOuter ref={ref} {...props}>
      <ContainerInner>{children}</ContainerInner>
    </ContainerOuter>
  )
})

```

# src/components/Button.tsx
```
import Link from 'next/link'
import clsx from 'clsx'

const variantStyles = {
  primary:
    'bg-zinc-800 font-semibold text-zinc-100 hover:bg-zinc-700 active:bg-zinc-800 active:text-zinc-100/70 dark:bg-zinc-700 dark:hover:bg-zinc-600 dark:active:bg-zinc-700 dark:active:text-zinc-100/70',
  secondary:
    'bg-zinc-50 font-medium text-zinc-900 hover:bg-zinc-100 active:bg-zinc-100 active:text-zinc-900/60 dark:bg-zinc-800/50 dark:text-zinc-300 dark:hover:bg-zinc-800 dark:hover:text-zinc-50 dark:active:bg-zinc-800/50 dark:active:text-zinc-50/70',
}

type ButtonProps = {
  variant?: keyof typeof variantStyles
} & (
  | (React.ComponentPropsWithoutRef<'button'> & { href?: undefined })
  | React.ComponentPropsWithoutRef<typeof Link>
)

export function Button({
  variant = 'primary',
  className,
  ...props
}: ButtonProps) {
  className = clsx(
    'inline-flex items-center gap-2 justify-center rounded-md py-2 px-3 text-sm outline-offset-2 transition active:transition-none',
    variantStyles[variant],
    className,
  )

  return typeof props.href === 'undefined' ? (
    <button className={className} {...props} />
  ) : (
    <Link className={className} {...props} />
  )
}

```

# src/components/Header.tsx
```
'use client'

import { Fragment, useEffect, useRef, useState } from 'react'
import Image from 'next/image'
import Link from 'next/link'
import { usePathname } from 'next/navigation'
import { useTheme } from 'next-themes'
import { Popover, Transition } from '@headlessui/react'
import clsx from 'clsx'

import { Container } from '@/components/Container'
import avatarImage from '@/images/avatar.jpg'

function CloseIcon(props: React.ComponentPropsWithoutRef<'svg'>) {
  return (
    <svg viewBox="0 0 24 24" aria-hidden="true" {...props}>
      <path
        d="m17.25 6.75-10.5 10.5M6.75 6.75l10.5 10.5"
        fill="none"
        stroke="currentColor"
        strokeWidth="1.5"
        strokeLinecap="round"
        strokeLinejoin="round"
      />
    </svg>
  )
}

function ChevronDownIcon(props: React.ComponentPropsWithoutRef<'svg'>) {
  return (
    <svg viewBox="0 0 8 6" aria-hidden="true" {...props}>
      <path
        d="M1.75 1.75 4 4.25l2.25-2.5"
        fill="none"
        strokeWidth="1.5"
        strokeLinecap="round"
        strokeLinejoin="round"
      />
    </svg>
  )
}

function SunIcon(props: React.ComponentPropsWithoutRef<'svg'>) {
  return (
    <svg
      viewBox="0 0 24 24"
      strokeWidth="1.5"
      strokeLinecap="round"
      strokeLinejoin="round"
      aria-hidden="true"
      {...props}
    >
      <path d="M8 12.25A4.25 4.25 0 0 1 12.25 8v0a4.25 4.25 0 0 1 4.25 4.25v0a4.25 4.25 0 0 1-4.25 4.25v0A4.25 4.25 0 0 1 8 12.25v0Z" />
      <path
        d="M12.25 3v1.5M21.5 12.25H20M18.791 18.791l-1.06-1.06M18.791 5.709l-1.06 1.06M12.25 20v1.5M4.5 12.25H3M6.77 6.77 5.709 5.709M6.77 17.73l-1.061 1.061"
        fill="none"
      />
    </svg>
  )
}

function MoonIcon(props: React.ComponentPropsWithoutRef<'svg'>) {
  return (
    <svg viewBox="0 0 24 24" aria-hidden="true" {...props}>
      <path
        d="M17.25 16.22a6.937 6.937 0 0 1-9.47-9.47 7.451 7.451 0 1 0 9.47 9.47ZM12.75 7C17 7 17 2.75 17 2.75S17 7 21.25 7C17 7 17 11.25 17 11.25S17 7 12.75 7Z"
        strokeWidth="1.5"
        strokeLinecap="round"
        strokeLinejoin="round"
      />
    </svg>
  )
}

function MobileNavItem({
  href,
  children,
}: {
  href: string
  children: React.ReactNode
}) {
  return (
    <li>
      <Popover.Button as={Link} href={href} className="block py-2">
        {children}
      </Popover.Button>
    </li>
  )
}

function MobileNavigation(
  props: React.ComponentPropsWithoutRef<typeof Popover>,
) {
  return (
    <Popover {...props}>
      <Popover.Button className="group flex items-center rounded-full bg-white/90 px-4 py-2 text-sm font-medium text-zinc-800 shadow-lg shadow-zinc-800/5 ring-1 ring-zinc-900/5 backdrop-blur dark:bg-zinc-800/90 dark:text-zinc-200 dark:ring-white/10 dark:hover:ring-white/20">
        Menu
        <ChevronDownIcon className="ml-3 h-auto w-2 stroke-zinc-500 group-hover:stroke-zinc-700 dark:group-hover:stroke-zinc-400" />
      </Popover.Button>
      <Transition.Root>
        <Transition.Child
          as={Fragment}
          enter="duration-150 ease-out"
          enterFrom="opacity-0"
          enterTo="opacity-100"
          leave="duration-150 ease-in"
          leaveFrom="opacity-100"
          leaveTo="opacity-0"
        >
          <Popover.Overlay className="fixed inset-0 z-50 bg-zinc-800/40 backdrop-blur-sm dark:bg-black/80" />
        </Transition.Child>
        <Transition.Child
          as={Fragment}
          enter="duration-150 ease-out"
          enterFrom="opacity-0 scale-95"
          enterTo="opacity-100 scale-100"
          leave="duration-150 ease-in"
          leaveFrom="opacity-100 scale-100"
          leaveTo="opacity-0 scale-95"
        >
          <Popover.Panel
            focus
            className="fixed inset-x-4 top-8 z-50 origin-top rounded-3xl bg-white p-8 ring-1 ring-zinc-900/5 dark:bg-zinc-900 dark:ring-zinc-800"
          >
            <div className="flex flex-row-reverse items-center justify-between">
              <Popover.Button aria-label="Close menu" className="-m-1 p-1">
                <CloseIcon className="h-6 w-6 text-zinc-500 dark:text-zinc-400" />
              </Popover.Button>
              <h2 className="text-sm font-medium text-zinc-600 dark:text-zinc-400">
                Navigation
              </h2>
            </div>
            <nav className="mt-6">
              <ul className="-my-2 divide-y divide-zinc-100 text-base text-zinc-800 dark:divide-zinc-100/5 dark:text-zinc-300">
                <MobileNavItem href="/about">About</MobileNavItem>
                <MobileNavItem href="/articles">Articles</MobileNavItem>
                <MobileNavItem href="/projects">Projects</MobileNavItem>
                <MobileNavItem href="/speaking">Speaking</MobileNavItem>
                <MobileNavItem href="/uses">Uses</MobileNavItem>
              </ul>
            </nav>
          </Popover.Panel>
        </Transition.Child>
      </Transition.Root>
    </Popover>
  )
}

function NavItem({
  href,
  children,
}: {
  href: string
  children: React.ReactNode
}) {
  let isActive = usePathname() === href

  return (
    <li>
      <Link
        href={href}
        className={clsx(
          'relative block px-3 py-2 transition',
          isActive
            ? 'text-teal-500 dark:text-teal-400'
            : 'hover:text-teal-500 dark:hover:text-teal-400',
        )}
      >
        {children}
        {isActive && (
          <span className="absolute inset-x-1 -bottom-px h-px bg-gradient-to-r from-teal-500/0 via-teal-500/40 to-teal-500/0 dark:from-teal-400/0 dark:via-teal-400/40 dark:to-teal-400/0" />
        )}
      </Link>
    </li>
  )
}

function DesktopNavigation(props: React.ComponentPropsWithoutRef<'nav'>) {
  return (
    <nav {...props}>
      <ul className="flex rounded-full bg-white/90 px-3 text-sm font-medium text-zinc-800 shadow-lg shadow-zinc-800/5 ring-1 ring-zinc-900/5 backdrop-blur dark:bg-zinc-800/90 dark:text-zinc-200 dark:ring-white/10">
        <NavItem href="/articles">Articles</NavItem>

        <NavItem href="/videos">Videos</NavItem>
      </ul>
    </nav>
  )
}

function ThemeToggle() {
  let { resolvedTheme, setTheme } = useTheme()
  let otherTheme = resolvedTheme === 'dark' ? 'light' : 'dark'
  let [mounted, setMounted] = useState(false)

  useEffect(() => {
    setMounted(true)
  }, [])

  return (
    <button
      type="button"
      aria-label={mounted ? `Switch to ${otherTheme} theme` : 'Toggle theme'}
      className="group rounded-full bg-white/90 px-3 py-2 shadow-lg shadow-zinc-800/5 ring-1 ring-zinc-900/5 backdrop-blur transition dark:bg-zinc-800/90 dark:ring-white/10 dark:hover:ring-white/20"
      onClick={() => setTheme(otherTheme)}
    >
      <SunIcon className="h-6 w-6 fill-zinc-100 stroke-zinc-500 transition group-hover:fill-zinc-200 group-hover:stroke-zinc-700 dark:hidden [@media(prefers-color-scheme:dark)]:fill-teal-50 [@media(prefers-color-scheme:dark)]:stroke-teal-500 [@media(prefers-color-scheme:dark)]:group-hover:fill-teal-50 [@media(prefers-color-scheme:dark)]:group-hover:stroke-teal-600" />
      <MoonIcon className="hidden h-6 w-6 fill-zinc-700 stroke-zinc-500 transition dark:block [@media(prefers-color-scheme:dark)]:group-hover:stroke-zinc-400 [@media_not_(prefers-color-scheme:dark)]:fill-teal-400/10 [@media_not_(prefers-color-scheme:dark)]:stroke-teal-500" />
    </button>
  )
}

function clamp(number: number, a: number, b: number) {
  let min = Math.min(a, b)
  let max = Math.max(a, b)
  return Math.min(Math.max(number, min), max)
}

function AvatarContainer({
  className,
  ...props
}: React.ComponentPropsWithoutRef<'div'>) {
  return (
    <div
      className={clsx(
        className,
        'h-10 w-10 rounded-full bg-white/90 p-0.5 shadow-lg shadow-zinc-800/5 ring-1 ring-zinc-900/5 backdrop-blur dark:bg-zinc-800/90 dark:ring-white/10',
      )}
      {...props}
    />
  )
}

function Avatar({
  large = false,
  className,
  ...props
}: Omit<React.ComponentPropsWithoutRef<typeof Link>, 'href'> & {
  large?: boolean
}) {
  return (
    <Link
      href="/"
      aria-label="Home"
      className={clsx(className, 'pointer-events-auto')}
      {...props}
    >
      <Image
        src={avatarImage}
        alt=""
        sizes={large ? '4rem' : '2.25rem'}
        className={clsx(
          'rounded-full bg-zinc-100 object-cover dark:bg-zinc-800',
          large ? 'h-16 w-16' : 'h-9 w-9',
        )}
        priority
      />
    </Link>
  )
}

export function Header() {
  let isHomePage = usePathname() === '/'

  let headerRef = useRef<React.ElementRef<'div'>>(null)
  let avatarRef = useRef<React.ElementRef<'div'>>(null)
  let isInitial = useRef(true)

  useEffect(() => {
    let downDelay = avatarRef.current?.offsetTop ?? 0
    let upDelay = 64

    function setProperty(property: string, value: string) {
      document.documentElement.style.setProperty(property, value)
    }

    function removeProperty(property: string) {
      document.documentElement.style.removeProperty(property)
    }

    function updateHeaderStyles() {
      if (!headerRef.current) {
        return
      }

      let { top, height } = headerRef.current.getBoundingClientRect()
      let scrollY = clamp(
        window.scrollY,
        0,
        document.body.scrollHeight - window.innerHeight,
      )

      if (isInitial.current) {
        setProperty('--header-position', 'sticky')
      }

      setProperty('--content-offset', `${downDelay}px`)

      if (isInitial.current || scrollY < downDelay) {
        setProperty('--header-height', `${downDelay + height}px`)
        setProperty('--header-mb', `${-downDelay}px`)
      } else if (top + height < -upDelay) {
        let offset = Math.max(height, scrollY - upDelay)
        setProperty('--header-height', `${offset}px`)
        setProperty('--header-mb', `${height - offset}px`)
      } else if (top === 0) {
        setProperty('--header-height', `${scrollY + height}px`)
        setProperty('--header-mb', `${-scrollY}px`)
      }

      if (top === 0 && scrollY > 0 && scrollY >= downDelay) {
        setProperty('--header-inner-position', 'fixed')
        removeProperty('--header-top')
        removeProperty('--avatar-top')
      } else {
        removeProperty('--header-inner-position')
        setProperty('--header-top', '0px')
        setProperty('--avatar-top', '0px')
      }
    }

    function updateAvatarStyles() {
      if (!isHomePage) {
        return
      }

      let fromScale = 1
      let toScale = 36 / 64
      let fromX = 0
      let toX = 2 / 16

      let scrollY = downDelay - window.scrollY

      let scale = (scrollY * (fromScale - toScale)) / downDelay + toScale
      scale = clamp(scale, fromScale, toScale)

      let x = (scrollY * (fromX - toX)) / downDelay + toX
      x = clamp(x, fromX, toX)

      setProperty(
        '--avatar-image-transform',
        `translate3d(${x}rem, 0, 0) scale(${scale})`,
      )

      let borderScale = 1 / (toScale / scale)
      let borderX = (-toX + x) * borderScale
      let borderTransform = `translate3d(${borderX}rem, 0, 0) scale(${borderScale})`

      setProperty('--avatar-border-transform', borderTransform)
      setProperty('--avatar-border-opacity', scale === toScale ? '1' : '0')
    }

    function updateStyles() {
      updateHeaderStyles()
      updateAvatarStyles()
      isInitial.current = false
    }

    updateStyles()
    window.addEventListener('scroll', updateStyles, { passive: true })
    window.addEventListener('resize', updateStyles)

    return () => {
      window.removeEventListener('scroll', updateStyles)
      window.removeEventListener('resize', updateStyles)
    }
  }, [isHomePage])

  return (
    <>
      <header
        className="pointer-events-none relative z-50 flex flex-none flex-col"
        style={{
          height: 'var(--header-height)',
          marginBottom: 'var(--header-mb)',
        }}
      >
        {isHomePage && (
          <>
            <div
              ref={avatarRef}
              className="order-last mt-[calc(theme(spacing.16)-theme(spacing.3))]"
            />
            <Container
              className="top-0 order-last -mb-3 pt-3"
              style={{
                position:
                  'var(--header-position)' as React.CSSProperties['position'],
              }}
            >
              <div
                className="top-[var(--avatar-top,theme(spacing.3))] w-full"
                style={{
                  position:
                    'var(--header-inner-position)' as React.CSSProperties['position'],
                }}
              >
                <div className="relative">
                  <AvatarContainer
                    className="absolute left-0 top-3 origin-left transition-opacity"
                    style={{
                      opacity: 'var(--avatar-border-opacity, 0)',
                      transform: 'var(--avatar-border-transform)',
                    }}
                  />
                  <Avatar
                    large
                    className="block h-16 w-16 origin-left"
                    style={{ transform: 'var(--avatar-image-transform)' }}
                  />
                </div>
              </div>
            </Container>
          </>
        )}
        <div
          ref={headerRef}
          className="top-0 z-10 h-16 pt-6"
          style={{
            position:
              'var(--header-position)' as React.CSSProperties['position'],
          }}
        >
          <Container
            className="top-[var(--header-top,theme(spacing.6))] w-full"
            style={{
              position:
                'var(--header-inner-position)' as React.CSSProperties['position'],
            }}
          >
            <div className="relative flex gap-4">
              <div className="flex flex-1">
                {!isHomePage && (
                  <AvatarContainer>
                    <Avatar />
                  </AvatarContainer>
                )}
              </div>
              <div className="flex flex-1 justify-end md:justify-center">
                <MobileNavigation className="pointer-events-auto md:hidden" />
                <DesktopNavigation className="pointer-events-auto hidden md:block" />
              </div>
              <div className="flex justify-end md:flex-1">
                <div className="pointer-events-auto">
                  <ThemeToggle />
                </div>
              </div>
            </div>
          </Container>
        </div>
      </header>
      {isHomePage && (
        <div
          className="flex-none"
          style={{ height: 'var(--content-offset)' }}
        />
      )}
    </>
  )
}

```

# src/components/Footer.tsx
```
import Link from 'next/link'

import { ContainerInner, ContainerOuter } from '@/components/Container'

function NavLink({
  href,
  children,
}: {
  href: string
  children: React.ReactNode
}) {
  return (
    <Link
      href={href}
      className="transition hover:text-teal-500 dark:hover:text-teal-400"
    >
      {children}
    </Link>
  )
}

export function Footer() {
  return (
    <footer className="mt-32 flex-none">
      <ContainerOuter>
        <div className="border-t border-zinc-100 pb-16 pt-10 dark:border-zinc-700/40">
          <ContainerInner>
            <div className="flex flex-col items-center justify-between gap-6 sm:flex-row">
              <div className="flex flex-wrap justify-center gap-x-6 gap-y-1 text-sm font-medium text-zinc-800 dark:text-zinc-200">
                <NavLink href="/articles">Articles</NavLink>
                <NavLink href="/videos">Videos</NavLink>
              </div>
              <p className="text-sm text-zinc-400 dark:text-zinc-500">
                &copy; {new Date().getFullYear()} ML Tinkering blog by Jerry
                Davis. Email: jerry@trainbox.ai
              </p>
            </div>
          </ContainerInner>
        </div>
      </ContainerOuter>
    </footer>
  )
}

```

# src/components/SocialIcons.tsx
```
export function XIcon(props: React.ComponentPropsWithoutRef<'svg'>) {
  return (
    <svg viewBox="0 0 24 24" aria-hidden="true" {...props}>
      <path d="M13.3174 10.7749L19.1457 4H17.7646L12.7039 9.88256L8.66193 4H4L10.1122 12.8955L4 20H5.38119L10.7254 13.7878L14.994 20H19.656L13.3171 10.7749H13.3174ZM11.4257 12.9738L10.8064 12.0881L5.87886 5.03974H8.00029L11.9769 10.728L12.5962 11.6137L17.7652 19.0075H15.6438L11.4257 12.9742V12.9738Z" />
    </svg>
  )
}

export function InstagramIcon(props: React.ComponentPropsWithoutRef<'svg'>) {
  return (
    <svg viewBox="0 0 24 24" aria-hidden="true" {...props}>
      <path d="M12 3c-2.444 0-2.75.01-3.71.054-.959.044-1.613.196-2.185.418A4.412 4.412 0 0 0 4.51 4.511c-.5.5-.809 1.002-1.039 1.594-.222.572-.374 1.226-.418 2.184C3.01 9.25 3 9.556 3 12s.01 2.75.054 3.71c.044.959.196 1.613.418 2.185.23.592.538 1.094 1.039 1.595.5.5 1.002.808 1.594 1.038.572.222 1.226.374 2.184.418C9.25 20.99 9.556 21 12 21s2.75-.01 3.71-.054c.959-.044 1.613-.196 2.185-.419a4.412 4.412 0 0 0 1.595-1.038c.5-.5.808-1.002 1.038-1.594.222-.572.374-1.226.418-2.184.044-.96.054-1.267.054-3.711s-.01-2.75-.054-3.71c-.044-.959-.196-1.613-.419-2.185A4.412 4.412 0 0 0 19.49 4.51c-.5-.5-1.002-.809-1.594-1.039-.572-.222-1.226-.374-2.184-.418C14.75 3.01 14.444 3 12 3Zm0 1.622c2.403 0 2.688.009 3.637.052.877.04 1.354.187 1.67.31.421.163.72.358 1.036.673.315.315.51.615.673 1.035.123.317.27.794.31 1.671.043.95.052 1.234.052 3.637s-.009 2.688-.052 3.637c-.04.877-.187 1.354-.31 1.67-.163.421-.358.72-.673 1.036a2.79 2.79 0 0 1-1.035.673c-.317.123-.794.27-1.671.31-.95.043-1.234.052-3.637.052s-2.688-.009-3.637-.052c-.877-.04-1.354-.187-1.67-.31a2.789 2.789 0 0 1-1.036-.673 2.79 2.79 0 0 1-.673-1.035c-.123-.317-.27-.794-.31-1.671-.043-.95-.052-1.234-.052-3.637s.009-2.688.052-3.637c.04-.877.187-1.354.31-1.67.163-.421.358-.72.673-1.036.315-.315.615-.51 1.035-.673.317-.123.794-.27 1.671-.31.95-.043 1.234-.052 3.637-.052Z" />
      <path d="M12 15a3 3 0 1 1 0-6 3 3 0 0 1 0 6Zm0-7.622a4.622 4.622 0 1 0 0 9.244 4.622 4.622 0 0 0 0-9.244Zm5.884-.182a1.08 1.08 0 1 1-2.16 0 1.08 1.08 0 0 1 2.16 0Z" />
    </svg>
  )
}

export function GitHubIcon(props: React.ComponentPropsWithoutRef<'svg'>) {
  return (
    <svg viewBox="0 0 24 24" aria-hidden="true" {...props}>
      <path
        fillRule="evenodd"
        clipRule="evenodd"
        d="M12 2C6.475 2 2 6.588 2 12.253c0 4.537 2.862 8.369 6.838 9.727.5.09.687-.218.687-.487 0-.243-.013-1.05-.013-1.91C7 20.059 6.35 18.957 6.15 18.38c-.113-.295-.6-1.205-1.025-1.448-.35-.192-.85-.667-.013-.68.788-.012 1.35.744 1.538 1.051.9 1.551 2.338 1.116 2.912.846.088-.666.35-1.115.638-1.371-2.225-.256-4.55-1.14-4.55-5.062 0-1.115.387-2.038 1.025-2.756-.1-.256-.45-1.307.1-2.717 0 0 .837-.269 2.75 1.051.8-.23 1.65-.346 2.5-.346.85 0 1.7.115 2.5.346 1.912-1.333 2.75-1.05 2.75-1.05.55 1.409.2 2.46.1 2.716.637.718 1.025 1.628 1.025 2.756 0 3.934-2.337 4.806-4.562 5.062.362.32.675.936.675 1.897 0 1.371-.013 2.473-.013 2.82 0 .268.188.589.688.486a10.039 10.039 0 0 0 4.932-3.74A10.447 10.447 0 0 0 22 12.253C22 6.588 17.525 2 12 2Z"
      />
    </svg>
  )
}

export function LinkedInIcon(props: React.ComponentPropsWithoutRef<'svg'>) {
  return (
    <svg viewBox="0 0 24 24" aria-hidden="true" {...props}>
      <path d="M18.335 18.339H15.67v-4.177c0-.996-.02-2.278-1.39-2.278-1.389 0-1.601 1.084-1.601 2.205v4.25h-2.666V9.75h2.56v1.17h.035c.358-.674 1.228-1.387 2.528-1.387 2.7 0 3.2 1.778 3.2 4.091v4.715zM7.003 8.575a1.546 1.546 0 01-1.548-1.549 1.548 1.548 0 111.547 1.549zm1.336 9.764H5.666V9.75H8.34v8.589zM19.67 3H4.329C3.593 3 3 3.58 3 4.297v15.406C3 20.42 3.594 21 4.328 21h15.338C20.4 21 21 20.42 21 19.703V4.297C21 3.58 20.4 3 19.666 3h.003z" />
    </svg>
  )
}

```

# src/components/Card.tsx
```
import Link from 'next/link'
import clsx from 'clsx'

function ChevronRightIcon(props: React.ComponentPropsWithoutRef<'svg'>) {
  return (
    <svg viewBox="0 0 16 16" fill="none" aria-hidden="true" {...props}>
      <path
        d="M6.75 5.75 9.25 8l-2.5 2.25"
        strokeWidth="1.5"
        strokeLinecap="round"
        strokeLinejoin="round"
      />
    </svg>
  )
}

export function Card<T extends React.ElementType = 'div'>({
  as,
  className,
  children,
}: Omit<React.ComponentPropsWithoutRef<T>, 'as' | 'className'> & {
  as?: T
  className?: string
}) {
  let Component = as ?? 'div'

  return (
    <Component
      className={clsx(className, 'group relative flex flex-col items-start')}
    >
      {children}
    </Component>
  )
}

Card.Link = function CardLink({
  children,
  ...props
}: React.ComponentPropsWithoutRef<typeof Link>) {
  return (
    <>
      <div className="absolute -inset-x-4 -inset-y-6 z-0 scale-95 bg-zinc-50 opacity-0 transition group-hover:scale-100 group-hover:opacity-100 sm:-inset-x-6 sm:rounded-2xl dark:bg-zinc-800/50" />
      <Link {...props}>
        <span className="absolute -inset-x-4 -inset-y-6 z-20 sm:-inset-x-6 sm:rounded-2xl" />
        <span className="relative z-10">{children}</span>
      </Link>
    </>
  )
}

Card.Title = function CardTitle<T extends React.ElementType = 'h2'>({
  as,
  href,
  children,
}: Omit<React.ComponentPropsWithoutRef<T>, 'as' | 'href'> & {
  as?: T
  href?: string
}) {
  let Component = as ?? 'h2'

  return (
    <Component className="text-base font-semibold tracking-tight text-zinc-800 dark:text-zinc-100">
      {href ? <Card.Link href={href}>{children}</Card.Link> : children}
    </Component>
  )
}

Card.Description = function CardDescription({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <p className="relative z-10 mt-2 text-sm text-zinc-600 dark:text-zinc-400">
      {children}
    </p>
  )
}

Card.Cta = function CardCta({ children }: { children: React.ReactNode }) {
  return (
    <div
      aria-hidden="true"
      className="relative z-10 mt-4 flex items-center text-sm font-medium text-teal-500"
    >
      {children}
      <ChevronRightIcon className="ml-1 h-4 w-4 stroke-current" />
    </div>
  )
}

Card.Eyebrow = function CardEyebrow<T extends React.ElementType = 'p'>({
  as,
  decorate = false,
  className,
  children,
  ...props
}: Omit<React.ComponentPropsWithoutRef<T>, 'as' | 'decorate'> & {
  as?: T
  decorate?: boolean
}) {
  let Component = as ?? 'p'

  return (
    <Component
      className={clsx(
        className,
        'relative z-10 order-first mb-3 flex items-center text-sm text-zinc-400 dark:text-zinc-500',
        decorate && 'pl-3.5',
      )}
      {...props}
    >
      {decorate && (
        <span
          className="absolute inset-y-0 left-0 flex items-center"
          aria-hidden="true"
        >
          <span className="h-4 w-0.5 rounded-full bg-zinc-200 dark:bg-zinc-500" />
        </span>
      )}
      {children}
    </Component>
  )
}

```

# src/components/ArticleLayout.tsx
```
'use client'

import { useContext } from 'react'
import { useRouter } from 'next/navigation'

import { AppContext } from '@/app/providers'
import { Container } from '@/components/Container'
import { Prose } from '@/components/Prose'
import { type ArticleWithSlug } from '@/lib/articles'
import { formatDate } from '@/lib/formatDate'

function ArrowLeftIcon(props: React.ComponentPropsWithoutRef<'svg'>) {
  return (
    <svg viewBox="0 0 16 16" fill="none" aria-hidden="true" {...props}>
      <path
        d="M7.25 11.25 3.75 8m0 0 3.5-3.25M3.75 8h8.5"
        strokeWidth="1.5"
        strokeLinecap="round"
        strokeLinejoin="round"
      />
    </svg>
  )
}

export function ArticleLayout({
  article,
  children,
}: {
  article: ArticleWithSlug
  children: React.ReactNode
}) {
  let router = useRouter()
  let { previousPathname } = useContext(AppContext)

  return (
    <Container className="mt-16 lg:mt-32">
      <div className="xl:relative">
        <div className="mx-auto max-w-2xl">
          {previousPathname && (
            <button
              type="button"
              onClick={() => router.back()}
              aria-label="Go back to articles"
              className="group mb-8 flex h-10 w-10 items-center justify-center rounded-full bg-white shadow-md shadow-zinc-800/5 ring-1 ring-zinc-900/5 transition lg:absolute lg:-left-5 lg:-mt-2 lg:mb-0 xl:-top-1.5 xl:left-0 xl:mt-0 dark:border dark:border-zinc-700/50 dark:bg-zinc-800 dark:ring-0 dark:ring-white/10 dark:hover:border-zinc-700 dark:hover:ring-white/20"
            >
              <ArrowLeftIcon className="h-4 w-4 stroke-zinc-500 transition group-hover:stroke-zinc-700 dark:stroke-zinc-500 dark:group-hover:stroke-zinc-400" />
            </button>
          )}
          <article>
            <header className="flex flex-col">
              <h1 className="mt-6 text-4xl font-bold tracking-tight text-zinc-800 sm:text-5xl dark:text-zinc-100">
                {article.title}
              </h1>
              <time
                dateTime={article.date}
                className="order-first flex items-center text-base text-zinc-400 dark:text-zinc-500"
              >
                <span className="h-4 w-0.5 rounded-full bg-zinc-200 dark:bg-zinc-500" />
                <span className="ml-3">{formatDate(article.date)}</span>
              </time>
            </header>
            <Prose className="mt-8" data-mdx-content>
              {children}
            </Prose>
          </article>
        </div>
      </div>
    </Container>
  )
}

```

