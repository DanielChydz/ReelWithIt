import React from "react";
import { render, screen } from "@testing-library/react";
import { MemoryRouter } from "react-router-dom";
import RatedMoviesList from "../../src/components/profile/RatedMoviesList";

describe("RatedMoviesList", () => {
  it("shows empty state", () => {
    render(
      <MemoryRouter>
        <RatedMoviesList loading={false} ratings={[]} />
      </MemoryRouter>
    );

    expect(screen.getByText("No rated movies yet.")).toBeInTheDocument();
  });

  it("renders ratings and movie link", () => {
    render(
      <MemoryRouter>
        <RatedMoviesList
          loading={false}
          ratings={[
            {
              rating: 8.5,
              movie_id: 42,
              title: "Interstellar",
              number_of_ratings: 230,
              user_id: 10,
            },
          ]}
        />
      </MemoryRouter>
    );

    expect(screen.getByText("Interstellar")).toBeInTheDocument();
    expect(screen.getByText("8.5")).toBeInTheDocument();
    expect(screen.getByRole("link", { name: /Interstellar/i })).toHaveAttribute(
      "href",
      "/movies/42"
    );
  });
});
