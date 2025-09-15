import Navbar from "../components/Navbar";

export default function ProfilePage() {
  return (
    <div className="min-h-screen bg-background font-sans">
      <header className="relative">
        <Navbar></Navbar>
      </header>

      <main className="p-8 flex flex-col gap-8"></main>
    </div>
  );
}
