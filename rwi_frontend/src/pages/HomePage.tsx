import { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import Navbar from "../components/Navbar";

type Movie = {
  id: number;
  title: string;
  director: string;
  year: number;
};

export default function HomePage() {
  const [movies, setMovies] = useState<Movie[]>([]);

  useEffect(() => {
    async function fetchMovies() {
      const res = await fetch("http://localhost:8000/movie/all");
      const data = await res.json();
      setMovies(data);
    }

    fetchMovies();
  }, []);

  /*return (
    <div className="min-h-screen bg-blue-100 p-0">
      <Navbar />
      <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-5 gap-6 pt-8 pl-8">
        {movies.map((movie) => (
          <div
            key={movie.id}
            className="bg-white rounded-lg shadow-blue-400 p-4 shadow-md hover:shadow-xl transition w-xs cursor-pointer"
          >
            <h6>{movie.id}</h6>
            <h2 className="text-xl font-semibold mb-2">{movie.title}</h2>
            <p className="text-gray-600">{movie.director}</p>
            <p className="text-gray-600">{movie.year}</p>
          </div>
        ))}
      </div>
      <div className="bg-surface p-6 rounded-2xl shadow-xl hover:shadow-2xl transition">
        <h2 className="text-primary text-2xl font-bold drop-shadow">Zaloguj się</h2>
        <input className="mt-4 p-2 rounded-lg bg-background border border-primary-light text-foreground shadow-inner" />
        <button className="mt-4 px-4 py-2 bg-primary text-white rounded-xl hover:bg-primary-dark hover:scale-105 transition transform shadow-md">
          Wejdź
        </button>
      </div>
    </div>
  );*/
  return (
    <div className="min-h-screen bg-background text-foreground font-sans">
      <header className="relative">
        <Navbar></Navbar>
      </header>

      <main className="p-8 flex flex-col gap-8">

      </main>
    </div>
  );
}
