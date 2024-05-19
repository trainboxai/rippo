Refactoring Plan
- Finding: Unused variable: The `logoHovered` state variable and the `setLogoHovered` function are defined in the RootLayoutContext, but never used.
    - Issue: Unnecessary state management and potential confusion for developers.
    - Refactoring Approach: Remove the `logoHovered` state variable and the `setLogoHovered` function from the `RootLayoutContext` and all related components.
    - Example:
        ```tsx
        // Before:
        const RootLayoutContext = createContext<{
          logoHovered: boolean
          setLogoHovered: React.Dispatch<React.SetStateAction<boolean>>
        } | null>(null)

        // After:
        const RootLayoutContext = createContext<null>(null)
        ```
    - Relevant Files: src/components/RootLayout.tsx
- Finding: Code duplication: The  XIcon, MenuIcon, FacebookIcon, InstagramIcon, and GitHubIcon components are duplicated across multiple files. This can lead to inconsistencies and maintenance overhead.
    - Issue: Increased maintenance effort and potential for inconsistencies when modifying the icons.
    - Refactoring Approach: Create a dedicated file for shared icons (e.g., `src/components/Icons.tsx`) and move all duplicated icon components to this file. Then, import and use the icons from this central location.
    - Example:
        ```tsx
        // src/components/Icons.tsx
        export function XIcon(props: React.ComponentPropsWithoutRef<'svg'>) {
          return (
            <svg viewBox="0 0 24 24" aria-hidden="true" {...props}>
              <path d="m5.636 4.223 14.142 14.142-1.414 1.414L4.222 5.637z" />
              <path d="M4.222 18.363 18.364 4.22l1.414 1.414L5.636 19.777z" />
            </svg>
          )
        }

        // ... other icons

        // src/components/RootLayout.tsx
        import { XIcon, MenuIcon } from '@/components/Icons'

        // ... use the icons
        ```
    - Relevant Files: src/components/RootLayout.tsx, src/components/Footer.tsx, src/components/SocialMedia.tsx
- Finding: Hardcoded values: In Logo.tsx, the width and height are hardcoded to 150. Consider defining them as constants for better readability and maintainability.
    - Issue: Reduced code readability and potential difficulty in adjusting logo dimensions.
    - Refactoring Approach: Define constants for the logo width and height within the `Logo.tsx` file.
    - Example:
        ```tsx
        // Before:
        const width = 150 // Logo width
        const height = 150 // Logo height

        // After:
        const LOGO_WIDTH = 150
        const LOGO_HEIGHT = 150

        // ... use the constants
        <Image
          src={logoPng}
          alt="Trainbox AI Logo"
          width={LOGO_WIDTH}
          height={LOGO_HEIGHT}
          style={{ objectFit: 'contain' }}
        />
        ```
    - Relevant Files: src/components/Logo.tsx
- Finding: Hardcoded social media links: The social media links in the Footer.tsx and SocialMedia.tsx components are hardcoded as '#' placeholders. This limits functionality and requires code changes to update the links.
    - Issue: Non-functional social media links and increased effort to update them in the future.
    - Refactoring Approach: Replace the '#' placeholders with actual social media links. Ideally, these links should be stored in a configuration file or environment variables to allow easy updates without code modifications.
    - Example:
        ```tsx
        // src/config.ts
        export const socialMediaLinks = {
          facebook: 'https://facebook.com/your-profile',
          instagram: 'https://instagram.com/your-profile',
          // ... other links
        }

        // src/components/Footer.tsx
        import { socialMediaLinks } from '@/config'

        // ... use the links
        <a key={item.name} href={socialMediaLinks[item.name.toLowerCase()]}>
        ```
    - Relevant Files: src/components/Footer.tsx, src/components/SocialMedia.tsx 
