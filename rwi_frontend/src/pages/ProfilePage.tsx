import { useEffect, useState } from "react";
import { useParams, useNavigate, useLocation } from "react-router-dom";
import Navbar from "../components/Navbar";
import { useAuthContext } from "../contexsts/AuthContext";
import ProfileHeader from "../components/profile/ProfileHeader";
import RatedMoviesList from "../components/profile/RatedMoviesList";

type User = {
  user_id: number;
  email: string;
  username: string;
  created_at: string;
  desc?: string | null;
};

type Rating = {
  rating: number;
  movie_id: number;
  title: string;
  number_of_ratings: number;
  user_id: number;
};

export default function ProfilePage() {
  const { username } = useParams<{ username?: string }>();
  const navigate = useNavigate();
  const location = useLocation();
  const auth = useAuthContext();

  const [user, setUser] = useState<User | null>(null);
  const [ratings, setRatings] = useState<Rating[]>([]);
  const [loadingUser, setLoadingUser] = useState(false);
  const [loadingRatings, setLoadingRatings] = useState(false);
  const [notFound, setNotFound] = useState(false);

  useEffect(() => {
    // Redirect logic for /profile and /me
    if (!username) {
      if (location.pathname === "/me" || location.pathname === "/profile") {
        if (auth.user) {
          navigate(`/profile/${auth.user.username}`, { replace: true });
        } else {
          navigate(`/auth/login`, { replace: true });
        }
      }
      return;
    }

    // Fetch user and ratings in parallel
    const base = "http://localhost:8000";
    let token = auth.accessToken;
    setLoadingUser(true);
    setLoadingRatings(true);
    setNotFound(false);

    const headers: Record<string, string> = {};
    if (token) headers["Authorization"] = `Bearer ${token}`;

    fetch(`${base}/user/${encodeURIComponent(username)}`, { headers })
      .then(async (res) => {
        if (res.status === 404) {
          setNotFound(true);
          setUser(null);
          return;
        }
        const data = await res.json();
        setUser(data);
      })
      .catch(() => setUser(null))
      .finally(() => setLoadingUser(false));

    fetch(`${base}/user/${encodeURIComponent(username)}/ratings`, { headers })
      .then(async (res) => {
        if (!res.ok) {
          setRatings([]);
          return;
        }
        const data = await res.json();
        setRatings(data as Rating[]);
      })
      .catch(() => setRatings([]))
      .finally(() => setLoadingRatings(false));
  }, [username, auth.user, auth.accessToken, navigate, location.pathname]);

  return (
    <div className="min-h-screen bg-background font-sans">
      <header className="relative">
        <Navbar />
      </header>

      <main className="p-8 flex flex-col gap-8">
        {notFound ? (
          <div className="text-center mt-8">User not found</div>
        ) : (
          <>
            <ProfileHeader
              loading={loadingUser}
              user={user}
              fallbackUsername={username || ""}
            />

            <section>
              <h2 className="text-xl font-semibold mb-4">Rated Movies</h2>
              <RatedMoviesList loading={loadingRatings} ratings={ratings} />
            </section>
          </>
        )}
      </main>
    </div>
  );
}
