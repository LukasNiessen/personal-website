/// <reference path="../.astro/types.d.ts" />
/// <reference types="astro/client" />

interface ImportMetaEnv {
  readonly IS_PRODUCTION: string;
}

interface ImportMeta {
  readonly env: ImportMetaEnv;
}
