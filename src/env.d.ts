/// <reference path="../.astro/types.d.ts" />
/// <reference types="astro/client" />

interface ImportMetaEnv {
  readonly IS_PRODUCTION: boolean;
}

interface ImportMeta {
  readonly env: ImportMetaEnv;
}
