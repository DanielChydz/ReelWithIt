import { Link } from "react-router-dom";

type Rating = {
  rating: number;
  movie_id: number;
  title: string;
  number_of_ratings: number;
  user_id: number;
};

export default function RatedMoviesList({
  loading,
  ratings,
}: {
  loading: boolean;
  ratings: Rating[];
}) {
  if (loading) {
    return (
      <div className="grid grid-cols-1 gap-3">
        {[1, 2, 3].map((i) => (
          <div key={i} className="p-4 bg-surface rounded shadow-sm animate-pulse" />
        ))}
      </div>
    );
  }

  if (!ratings || ratings.length === 0) {
    return <div>No rated movies yet.</div>;
  }

  return (
    <div className="grid grid-cols-1 gap-3">
      {ratings.map((r) => (
        <Link
          to={`/movies/${r.movie_id}`}
          key={r.movie_id}
          className="p-4 bg-surface rounded hover:shadow-md flex justify-between items-center"
        >
          <div>
            <div className="font-semibold">{r.title}</div>
            <div className="text-sm text-foreground-muted">{r.number_of_ratings} ratings</div>
          </div>
          <div className="text-right">
            <div className="text-lg font-bold">{r.rating.toFixed(1)}</div>
          </div>
        </Link>
      ))}
    </div>
  );
}
