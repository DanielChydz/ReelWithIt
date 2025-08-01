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
