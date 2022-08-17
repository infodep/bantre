import { createContext, Dispatch, SetStateAction, useEffect, useState } from "react";
import jwt_decode from "jwt-decode";
import { Token } from "../interfaces/Token";
import { Tokens } from "../interfaces/Tokens";
import axios from "axios";

interface Props {
  children: React.ReactNode;
}

interface ContextData {
  user_id: number | null;
  authTokens: Tokens;
  setAuthTokens: Dispatch<SetStateAction<Tokens>>;
  setUser: Dispatch<number | null>;
  loginUser: (username: string, password: string, url?: string | undefined) => Promise<void>;
  logoutUser: () => Promise<void>;
}

const initialData: ContextData = {
  user_id: null,
  authTokens: { refresh_token: null, access_token: null },
  setAuthTokens: (): void => {
    throw new Error("setAuthTokens function must be overridden");
  },
  setUser: (): void => {
    throw new Error("setUser function must be overridden");
  },
  loginUser: () => {
    throw new Error("loginUser function must be overridden");
  },
  logoutUser: () => {
    throw new Error("logoutUser function must be overridden");
  },
};

const AuthContext = createContext(initialData);

export default AuthContext;

export const AuthProvider = ({ children }: Props): JSX.Element => {
  const refresh_token = typeof window !== "undefined" ? window.localStorage.getItem("refresh_token") : null;
  const [authTokens, setAuthTokens] = useState<Tokens>({ refresh_token, access_token: null });
  const [user_id, setUser] = useState<number | null>(() =>
    refresh_token ? jwt_decode<Token>(refresh_token).id : null,
  );
  const [loading, setLoading] = useState(true);
  //const router = useRouter();

  const loginUser = async (username: string, password: string, url?: string) => {
    await axios
      .post("/v1/login", {
        username: username,
        password: password,
      })
      .then((res) => {
        return res.data;
      })
      .then((data) => {
        window.localStorage.setItem("refresh_token", data["refresh-token"]);
        setAuthTokens(data);
        setUser(jwt_decode<Token>(data["access-token"]).id);

        // if (!url) url = "/";
        // router.push(url);
        console.log(url);
      })
      .catch((err) => {
        throw new Error(err.message);
      });
  };

  const logoutUser = async () => {
    setAuthTokens({ refresh_token: null, access_token: null });
    setUser(null);
    window.localStorage.removeItem("refresh_token");
    // router.push("/login");
  };

  const contextData = {
    user_id: user_id,
    authTokens: authTokens,
    setAuthTokens: setAuthTokens,
    setUser: setUser,
    loginUser: loginUser,
    logoutUser: logoutUser,
  };

  useEffect(() => {
    if (authTokens.refresh_token) {
      setUser(jwt_decode<Token>(authTokens.refresh_token).id);
    }
    setLoading(false);
  }, [authTokens, loading]);

  return <AuthContext.Provider value={contextData}>{loading ? null : children}</AuthContext.Provider>;
};
