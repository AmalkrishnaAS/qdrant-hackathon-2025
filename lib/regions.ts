export const REGION_LABELS: Record<string, string> = {
  US: 'United States',
  IN: 'India',
  GB: 'United Kingdom',
  DE: 'Germany',
  FR: 'France',
  JP: 'Japan',
  BR: 'Brazil',
  CA: 'Canada',
  AU: 'Australia',
  AE: 'United Arab Emirates',
};

export function formatRegionLabel(code: string | undefined): string {
  if (!code) return 'Unknown';
  const upper = code.toUpperCase();
  const name = REGION_LABELS[upper] ?? upper;
  return `${name} (${upper})`;
}


