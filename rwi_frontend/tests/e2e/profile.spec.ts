import { test, expect } from "@playwright/test";

test("shows public profile with rated movies", async ({ page }) => {
  await page.route("http://localhost:8000/user/john", async (route) => {
    await route.fulfill({
      status: 200,
      contentType: "application/json",
      body: JSON.stringify({
        user_id: 10,
        email: "john@example.com",
        username: "john",
        created_at: "2026-02-22T10:00:00Z",
        desc: "movie nerd",
      }),
    });
  });

  await page.route("http://localhost:8000/user/john/ratings", async (route) => {
    await route.fulfill({
      status: 200,
      contentType: "application/json",
      body: JSON.stringify([
        {
          rating: 8.5,
          movie_id: 42,
          title: "Interstellar",
          number_of_ratings: 230,
          user_id: 10,
        },
      ]),
    });
  });

  await page.route("http://localhost:8000/media/profiles/10", async (route) => {
    await route.fulfill({ status: 404 });
  });

  await page.goto("/profile/john");

  await expect(page.getByRole("heading", { name: "john" })).toBeVisible();
  await expect(page.getByText("movie nerd")).toBeVisible();
  await expect(page.getByText("Interstellar")).toBeVisible();
  await expect(page.getByRole("link", { name: /Interstellar/i })).toHaveAttribute(
    "href",
    "/movies/42"
  );
  await expect(page.getByRole("img", { name: "john avatar" })).toHaveAttribute(
    "src",
    /data:image\/svg\+xml/
  );
});
