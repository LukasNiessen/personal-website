type Uniform<T> = { value: T };
type ShaderMaterial = {
  fragmentShader: string;
  uniforms: Record<string, Uniform<unknown>>;
  needsUpdate: boolean;
};

export type FogEffect = {
  destroy: () => void;
  scene: { children: { material?: ShaderMaterial }[] };
  camera: unknown;
  renderer: { domElement: HTMLCanvasElement; render: (scene: unknown, camera: unknown) => void };
  onUpdate?: () => void;
};

export type FogPointer = { x: number; y: number; active: boolean };

// Add detail to the existing noise field, rather than painting a lens over it.
// Only the existing shader/material is used; there is no extra WebGL context.
export function addFogFocus(effect: FogEffect, pointer: FogPointer) {
  const material = effect.scene.children.find((child) => child.material?.fragmentShader)?.material;
  if (!material) return;

  const focus = { value: { x: 0.5, y: 0.5 } };
  const size = { value: { x: 1, y: 1 } };
  const resolution = { value: { x: effect.renderer.domElement.width, y: effect.renderer.domElement.height } };
  const strength = { value: 0 };
  Object.assign(material.uniforms, {
    focusPosition: focus, focusSize: size, focusResolution: resolution, focusStrength: strength,
  });
  material.fragmentShader = `
    uniform vec2 focusPosition;
    uniform vec2 focusSize;
    uniform vec2 focusResolution;
    uniform float focusStrength;
    float detailStrength;
  ` + material.fragmentShader
    .replace("float a = blurFactor;", "float a = blurFactor;\n  float detailWeight = 0.055;")
    .replace("v += a * noise(_st);", `
      float sampleValue = noise(_st);
      v += a * sampleValue;
      if (i >= 2) {
        v += detailStrength * detailWeight * (sampleValue - 0.5);
        detailWeight *= 0.5;
      }
    `)
    .replace("void main() {", `void main() {
      detailStrength = 0.0;
      vec2 fragmentPosition = gl_FragCoord.xy / focusResolution;
      float distanceToPointer = length((fragmentPosition - focusPosition) * focusSize);
      float clarity = (1.0 - smoothstep(0.0, 44.0, distanceToPointer)) * focusStrength;
    `)
    // Preserve the cloud shape and low-frequency color fields. Only the final
    // density sample receives centered high-frequency detail near the pointer.
    .replace("float f = fbm(st+r);", "detailStrength = clarity;\n  float f = fbm(st+r);")
    .replace("vec4(finalColor,1.0)", "vec4(finalColor * 0.965,1.0)");
  material.needsUpdate = true;

  const previousUpdate = effect.onUpdate;
  effect.onUpdate = () => {
    previousUpdate?.call(effect);
    const targetStrength = pointer.active ? 1 : 0;
    strength.value += (targetStrength - strength.value) * 0.18;
    if (strength.value < 0.001 && !pointer.active) {
      strength.value = 0;
      return;
    }
    // The canvas rect includes the pan/scale, so the 88px footprint stays fixed
    // in CSS pixels on retina screens and follows the pointer during scrolling.
    const canvas = effect.renderer.domElement;
    const rect = canvas.getBoundingClientRect();
    resolution.value.x = canvas.width;
    resolution.value.y = canvas.height;
    size.value.x = rect.width;
    size.value.y = rect.height;
    focus.value.x = (pointer.x - rect.left) / rect.width;
    focus.value.y = 1 - (pointer.y - rect.top) / rect.height;
  };
  effect.renderer.render(effect.scene, effect.camera);
}
