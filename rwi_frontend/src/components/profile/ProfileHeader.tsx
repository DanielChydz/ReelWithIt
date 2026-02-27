import type { userData } from "../../types/auth";
import { generateAvatarDataUrl } from "../../utils/avatar";

type Props = {
  loading: boolean;
  user: (userData & { desc?: string | null }) | null;
  fallbackUsername: string;
};

export default function ProfileHeader({ loading, user, fallbackUsername }: Props) {
  const username = user?.username ?? fallbackUsername;
  const desc = user?.desc ?? null;
  const userId = user?.user_id;

  const imgSrc = userId ? `http://localhost:8000/media/profiles/${userId}` : undefined;

  return (
    <header className="flex items-center gap-6">
      <div className="w-24 h-24">
        {loading ? (
          <div className="w-24 h-24 bg-gray-200 animate-pulse rounded-full" />
        ) : (
          <img
            src={imgSrc}
            alt={`${username} avatar`}
            onError={(e) => {
              const target = e.currentTarget as HTMLImageElement;
              target.onerror = null;
              target.src = generateAvatarDataUrl(username);
            }}
            className="w-24 h-24 rounded-full object-cover"
          />
        )}
      </div>

      <div>
        <h1 className="text-2xl font-bold">{username}</h1>
        {loading ? (
          <div className="w-64 h-4 bg-gray-200 rounded mt-2 animate-pulse" />
        ) : (
          <p className="text-sm text-foreground-muted mt-2">{desc ?? ""}</p>
        )}
      </div>
    </header>
  );
}
