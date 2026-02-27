function hashCode(str: string): number {
  let hash = 0;
  for (let i = 0; i < str.length; i++) {
    hash = (hash << 5) - hash + str.charCodeAt(i);
    hash |= 0;
  }
  return Math.abs(hash);
}

const COLORS = [
  "#F97316",
  "#F43F5E",
  "#60A5FA",
  "#34D399",
  "#A78BFA",
  "#FBBF24",
  "#FB7185",
  "#7C3AED",
];

export function generateAvatarDataUrl(username: string): string {
  const letter = username && username.length > 0 ? username[0].toUpperCase() : "?";
  const idx = hashCode(username || "") % COLORS.length;
  const bg = COLORS[idx];
  const svg = `<?xml version='1.0' encoding='UTF-8'?>
  <svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 128 128' width='128' height='128'>
    <circle cx='64' cy='64' r='64' fill='${bg}' />
    <text x='50%' y='50%' font-family='Arial, Helvetica, sans-serif' font-size='64' fill='white' text-anchor='middle' dominant-baseline='middle'>${letter}</text>
  </svg>`;

  return `data:image/svg+xml;utf8,${encodeURIComponent(svg)}`;
}

export default generateAvatarDataUrl;
