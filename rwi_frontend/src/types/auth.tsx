export type userLoginData = {
  email: string;
  password: string;
};

export type userRegisterData = {
  email: string;
  username: string;
  password: string;
};

export type userData = {
  user_id: number;
  email: string;
  username: string;
  created_at: string; // ISO 8601 (aware datetime)
};

export type AuthContextType = {
  user: userData | null;
  accessToken: string | null;
  logIn: (user: userLoginData) => Promise<void>;
  logOut: () => void;
  register: (user: userRegisterData) => Promise<void>;
};
