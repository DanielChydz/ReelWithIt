import { generateAvatarDataUrl } from "../../src/utils/avatar";

describe("generateAvatarDataUrl", () => {
  it("returns svg data url", () => {
    const url = generateAvatarDataUrl("john");
    expect(url.startsWith("data:image/svg+xml;utf8,")).toBe(true);
  });

  it("contains uppercase first letter", () => {
    const url = generateAvatarDataUrl("john");
    const decoded = decodeURIComponent(url.replace("data:image/svg+xml;utf8,", ""));
    expect(decoded).toContain(">J<");
    expect(decoded).toContain("<circle");
  });
});
