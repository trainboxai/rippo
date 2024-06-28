# package.json
```
{
  "name": "nuxt-app",
  "private": true,
  "type": "module",
  "scripts": {
    "build": "nuxt build",
    "dev": "nuxt dev",
    "generate": "nuxt generate",
    "preview": "nuxt preview",
    "postinstall": "nuxt prepare"
  },
  "devDependencies": {
    "autoprefixer": "^10.4.17",
    "nuxt": "^3.9.3",
    "postcss": "^8.4.33",
    "tailwindcss": "^3.4.1",
    "vue": "^3.4.14",
    "vue-router": "^4.2.5"
  },
  "dependencies": {}
}

```

# nuxt.config.ts
```

export default defineNuxtConfig({
  devtools: { enabled: true },

  css: ['~/assets/css/main.css'],
  
  app: {
    head: {
      link: [
        { rel: 'manifest', href: '/manifest.json', type: 'application/manifest+json' }
      ]
    }
  },

  postcss: {
    plugins: {
      tailwindcss: {},
      autoprefixer: {},
    },
  },
})

```

# tailwind.config.js
```
/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./components/**/*.{js,vue,ts}",
    "./layouts/**/*.vue",
    "./pages/**/*.vue",
    "./plugins/**/*.{js,ts}",
    "./app.vue",
    "./error.vue",
  ],
  theme: {
    extend: {},
  },
  plugins: [],
}


```

# tsconfig.json
```
{
  // https://nuxt.com/docs/guide/concepts/typescript
  "extends": "./.nuxt/tsconfig.json"
}

```

# app.vue
```
<template>

    <div>
      <NuxtPage />
    </div>
  </template>
  




<script setup>
import { onMounted } from 'vue';

onMounted(() => {
  if (process.client && 'serviceWorker' in navigator) {
    navigator.serviceWorker.register('/service-worker.js')
      .then(registration => {
        console.log('Service Worker registered with scope:', registration.scope);
      })
      .catch(err => {
        console.error('Service Worker registration failed:', err);
      });
  }
});
</script>

```

# pwa.config.ts
```
import type { VitePWAOptions } from 'vite-plugin-pwa';

const pwaConfig: VitePWAOptions = {
  registerType: 'autoUpdate',
  devOptions: {
    enabled: true
  },
  workbox: {
    // Workbox options
  },
  manifest: {
    name: 'My PWA',
    short_name: 'PWA',
    theme_color: '#ffffff',
    icons: [
      {
        src: '/icon-192x192.png', // put your icon in the public folder
        sizes: '192x192',
        type: 'image/png',
      },
      {
        src: '/icon-512x512.png',
        sizes: '512x512',
        type: 'image/png',
      },
    ],
  },
} as VitePWAOptions;

export default pwaConfig

```

# commit-push.sh
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

# assets/css/main.css
```
/* Importing Google font - Inter */
@import url("https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap");
@tailwind base;
@tailwind components;
@tailwind utilities;

* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
  font-family: "Inter", sans-serif;
}

body {
  height: 100vh;
  align-items: center;
  justify-content: center;
  background: #1d1e23;
}

.w-container {
  margin-left: auto;
  margin-right: auto;
  max-width: 1280px;
  padding: 4rem;
}

h2 {
  color: #fff;
  font-size: 2rem;
  font-weight: 600;
}

h2 span {
  color: #bd53ed;
  position: relative;
}

h2 span::before {
  content: "";
  height: 30px;
  width: 2px;
  position: absolute;
  top: 50%;
  right: -8px;
  background: #bd53ed;
  transform: translateY(-45%);
  animation: blink 0.7s infinite;
}

h2 span.stop-blinking::before {
  animation: none;
}

@keyframes blink {
  50% {
    opacity: 0;
  }
}

```

# server/tsconfig.json
```
{
  "extends": "../.nuxt/tsconfig.server.json"
}

```

# public/service-worker.js
```
self.addEventListener('fetch', function(event) {
    event.respondWith(
      caches.match(event.request).then(function(response) {
        return response || fetch(event.request);
      })
    );
  });
  
```

# public/manifest.json
```
{
    "name": "My App Name",
    "short_name": "App",
    "start_url": "/",
    "display": "standalone",
    "theme_color": "#ffffff",
    "background_color": "#ffffff",
    "icons": [
      {
        "src": "/icon-192x192.png",
        "sizes": "192x192",
        "type": "image/png"
      },
      {
        "src": "/icon-512x512.png",
        "sizes": "512x512",
        "type": "image/png"
      }
    ]
  }
  
```

# pages/index.vue
```
<template>
  <div class="bg-white">
    <div class="mx-auto max-w-7xl py-24 sm:px-6 sm:py-32 lg:px-8">
      <div
        class="relative isolate overflow-hidden bg-gray-900 px-6 py-24 text-center shadow-2xl sm:rounded-3xl sm:px-16"
      >
        <h2
          class="mx-auto max-w-2xl text-3xl font-bold tracking-tight text-indigo-100 sm:text-4xl mb-8"
        >
          Speak?<span ref="animatedText"></span>
        </h2>
        <h2
          class="mx-auto max-w-2xl text-xl font-bold tracking-tight text-indigo-100 sm:text-2xl"
        >
          Transform Your Language Learning Experience with AI
        </h2>
        <p class="mx-auto mt-6 max-w-xl text-lg leading-8 text-gray-300">
          Speak?Yes! brings your language learning to life with AI-powered
          conversations and natural-sounding voices. Practice anytime, anywhere
          without fear of making mistakes, and receive personalized feedback to
          boost your skills.
        </p>

        <div class="mt-10 flex items-center justify-center gap-x-6">
          <form
            @submit.prevent="submitEmail"
            class="w-full max-w-md flex items-center justify-center mb-4"
          >
            <div class="flex gap-x-4">
              <label for="email-address" class="sr-only">Email address</label>
              <input
                id="email-address"
                name="email"
                type="email"
                autocomplete="email"
                required=""
                class="min-w-0 flex-auto rounded-md border-0 bg-white/5 px-3.5 py-2 text-white shadow-sm ring-1 ring-inset ring-white/10 focus:ring-2 focus:ring-inset focus:ring-white sm:text-sm sm:leading-6"
                placeholder="Enter your email"
              />
              <button
                type="submit"
                class="flex-none rounded-md bg-white px-3.5 py-2.5 text-sm font-semibold text-gray-900 shadow-sm hover:bg-gray-100 focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-white"
              >
                Join waitlist
              </button>
            </div>
          </form>
        </div>
        <span class="text-lg mt-12 text-indigo-100">{{ responseMessage }}</span>

        <svg
          viewBox="0 0 1024 1024"
          class="absolute left-1/2 top-1/2 -z-10 h-[64rem] w-[64rem] -translate-x-1/2 [mask-image:radial-gradient(closest-side,white,transparent)]"
          aria-hidden="true"
        >
          <circle
            cx="512"
            cy="512"
            r="512"
            fill="url(#827591b1-ce8c-4110-b064-7cb85a0b1217)"
            fill-opacity="0.7"
          />
          <defs>
            <radialGradient id="827591b1-ce8c-4110-b064-7cb85a0b1217">
              <stop stop-color="#7775D6" />
              <stop offset="1" stop-color="#E935C1" />
            </radialGradient>
          </defs>
        </svg>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      words: ["Ja!", "Sí!", "Sim!", "Oui!", "Да!", "Yes!", "Áno!"],
      wordIndex: 0,
      charIndex: 0,
      isDeleting: false,
      responseMessage: "",
    };
  },
  mounted() {
    this.typeEffect();
  },

  methods: {
    async submitEmail(event) {
      event.preventDefault();
      const formData = new FormData(event.target);
      try {
        const response = await fetch(
          "https://speakyes.ew.r.appspot.com/submit_email/",
          {
            method: "POST",
            body: formData,
          }
        );
        const data = await response.json();
        this.responseMessage = "Email received. Thank you!";
      } catch (error) {
        console.error("Error:", error);
        this.responseMessage = "An error occurred.";
      }
    },

    typeEffect() {
      const currentWord = this.words[this.wordIndex];
      const currentChar = currentWord.substring(0, this.charIndex);
      this.$refs.animatedText.textContent = currentChar;
      this.$refs.animatedText.classList.add("stop-blinking");

      if (!this.isDeleting && this.charIndex < currentWord.length) {
        this.charIndex++;
        setTimeout(this.typeEffect, 200);
      } else if (this.isDeleting && this.charIndex > 0) {
        this.charIndex--;
        setTimeout(this.typeEffect, 100);
      } else {
        this.isDeleting = !this.isDeleting;
        this.$refs.animatedText.classList.remove("stop-blinking");
        this.wordIndex = !this.isDeleting
          ? (this.wordIndex + 1) % this.words.length
          : this.wordIndex;
        setTimeout(this.typeEffect, 1200);
      }
    },
    async startSession() {
      this.$router.push("/shopping");
    },
  },
};
</script>

```

