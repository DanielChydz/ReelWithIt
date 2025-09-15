import { Link, useNavigate } from "react-router-dom";
import { useAuthContext } from "../contexsts/AuthContext";

export default function Navbar() {
  let navigate = useNavigate();
  const authCtx = useAuthContext();

  return (
    <div className="relative z-10 bg-gradient-to-b from-surface to-background px-6 py-4 shadow-sm flex justify-between items-center text-foreground">
      <div className="flex basis-1/3 justify-start items-center gap-4 pl-4 font-bold text-lg">
        <Link
          to="/"
          className="text-4xl font-bold text-center text-primary hover:text-primary-dark transition"
        >
          🎬 ReelWithIt
        </Link>
      </div>
      <div className="flex basis-1/3 justify-center items-center gap-4 pl-4 font-bold text-lg">
        <input
          placeholder="Search for a movie..."
          className="box-border border-1 rounded-4xl p-1 pl-4 pr-4 w-96 hover:bg-surface focus:border-2 focus:outline-none transition"
        ></input>
      </div>
      {authCtx.user ? (
        <div className="flex basis-1/3 justify-end items-center gap-4 pl-4 font-bold text-lg">
          <button
            onClick={async () => {
              authCtx.logOut();
              navigate("/", { replace: true });
            }}
            className="text-white hover:text-foreground text-sm font-medium cursor-pointer transition hover:bg-primary-dark rounded-4xl pl-1 pr-1"
          >
            Log Out
          </button>

          <button
            onClick={() => navigate("/profile")}
            className="bg-primary hover:bg-primary-dark text-foreground px-4 py-1 rounded-4xl cursor-pointer transition"
          >
            {authCtx.user.username}
          </button>
        </div>
      ) : (
        <div className="flex basis-1/3 justify-end items-center gap-4 pl-4 font-bold text-lg">
          <button
            onClick={() => navigate("/auth/login")}
            className="text-foreground px-4 py-1 rounded-4xl box-border border-1 hover:bg-surface cursor-pointer transition"
          >
            Log In
          </button>
          <button
            onClick={() => navigate("/auth/register")}
            className="bg-primary hover:bg-primary-dark text-white px-4 py-1 rounded-4xl cursor-pointer transition"
          >
            Sign Up
          </button>
        </div>
      )}
    </div>
  );
}
