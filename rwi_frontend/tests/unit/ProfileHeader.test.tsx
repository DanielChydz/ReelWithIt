import React from "react";
import { fireEvent, render, screen } from "@testing-library/react";
import ProfileHeader from "../../src/components/profile/ProfileHeader";

describe("ProfileHeader", () => {
  it("renders username and desc", () => {
    render(
      <ProfileHeader
        loading={false}
        fallbackUsername="fallback"
        user={{
          user_id: 10,
          email: "john@example.com",
          username: "john",
          created_at: "2026-02-22T10:00:00Z",
          desc: "movie nerd",
        }}
      />
    );

    expect(screen.getByRole("heading", { name: "john" })).toBeInTheDocument();
    expect(screen.getByText("movie nerd")).toBeInTheDocument();
    expect(screen.getByAltText("john avatar")).toHaveAttribute(
      "src",
      "http://localhost:8000/media/profiles/10"
    );
  });

  it("falls back to generated avatar when image fails", () => {
    render(
      <ProfileHeader
        loading={false}
        fallbackUsername="john"
        user={{
          user_id: 10,
          email: "john@example.com",
          username: "john",
          created_at: "2026-02-22T10:00:00Z",
          desc: null,
        }}
      />
    );

    const image = screen.getByAltText("john avatar") as HTMLImageElement;
    fireEvent.error(image);

    expect(image.src).toContain("data:image/svg+xml");
  });
});
