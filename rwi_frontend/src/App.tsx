import { useEffect, useState } from "react";
import { Link } from "react-router-dom";

type Movie = {
  id: number;
  title: string;
  director: string;
  year: number;
}

export default function HomePage() {
  const [movies, setMovies] = useState<Movie[]>([]);
  const [isLoggedIn, setIsLoggedIn] = useState(false);
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [userData, setUserData] = useState<any>(null);

  async function logIn() {
    const loginData = new URLSearchParams();
    loginData.append("username", email);
    loginData.append("password", password);
    try{
      const res = await fetch("http://localhost:8000/auth/login",
      {
        method: "POST",
        headers: { "Content-Type": "application/x-www-form-urlencoded" },
        body: loginData,
      });
      
      if (!res.ok) throw new Error("Login error");

      setUserData(await res.json())
      setIsLoggedIn(true);
      setPassword("");
    } catch (err) {
      setEmail("");
      setPassword("");
    }
  }

  function logOut() {
    setIsLoggedIn(false);
    setEmail("");
    setPassword("");
  }

  useEffect(() => {
    async function fetchMovies() {
      const res = await fetch("http://localhost:8000/movie/all");
      const data = await res.json();
      setMovies(data);
    }

    fetchMovies();
  }, []);

  return (
    <div className="min-h-screen bg-blue-100 p-0">
      <div className="flex items-center justify-between bg-blue-300 pb-4 pt-4 border-b-0 shadow-md shadow-blue-400">
        <div className="flex basis-1/3 justify-start items-center gap-4 pl-4">
          <input
            className="bg-white hover:bg-gray-200 rounded-xl box-border w-52 pl-4 pr-4 pt-1 pb-1"
            placeholder="Movie data"
          />
          <button className="bg-blue-400 hover:bg-blue-500 text-white py-2 px-4 rounded cursor-pointer">
            Search
          </button>
        </div>
        <div className="flex basis-1/3 justify-center items-center">
          <Link to="/" className="text-4xl font-bold text-center text-blue-600">
            ReelWithIt
          </Link>
        </div>
        {isLoggedIn ? (
          <div className="flex basis-1/3 justify-end items-center pr-4 gap-4">
            <h3 className="text-blue-600">
              {userData?.user.username}
            </h3>
            <button 
              onClick={logOut}
              className="bg-blue-400 hover:bg-blue-500 text-white py-2 px-4 rounded cursor-pointer"
            >
              Log out
            </button>
          </div>
        ) : (
          <div className="flex basis-1/3 justify-end items-center pr-4 gap-4">
            <form onSubmit={(e) => {
                e.preventDefault();
                logIn();
              }}
              className="flex gap-4 items-center"
            >
              <input 
                value={email}
                onChange={(event) => setEmail(event.currentTarget.value)}
                className="bg-white hover:bg-gray-200 rounded-xl box-border w-52 pl-4 pr-4 pt-1 pb-1"
                placeholder="E-mail"
              />
              <input
                value={password}
                onChange={(event) => setPassword(event.currentTarget.value)}
                className="bg-white hover:bg-gray-200 rounded-xl box-border w-52 pl-4 pr-4 pt-1 pb-1"
                placeholder="Password"
                type="password"
              />
              <button
                type="submit"
                onClick={logIn}
                className="bg-blue-400 hover:bg-blue-500 text-white py-2 px-4 rounded cursor-pointer"
              >
                Log in
              </button>
            </form>
          </div>
        )}
      </div>
      <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-5 gap-6 pt-8 pl-8">
        {movies.map((movie) => (
          <div
            key={movie.id}
            className="bg-white rounded-lg shadow-blue-400 shadow-md p-4 hover:shadow-xl transition w-xs cursor-pointer"
          >
            <h6>{movie.id}</h6>
            <h2 className="text-xl font-semibold mb-2">{movie.title}</h2>
            <p className="text-gray-600">{movie.director}</p>
            <p className="text-gray-600">{movie.year}</p>
          </div>
        ))}
      </div>
    </div>
  );
}