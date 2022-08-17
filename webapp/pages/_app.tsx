import "../styles/globals.css";
import type { AppProps } from "next/app";
import axios from "axios";
import { AuthProvider } from "../contexts/auth";

//Define NEXT_PUBLIC_BASE_URL in .env.local, next will automatically import
axios.defaults.baseURL = process.env.NEXT_PUBLIC_BASE_URL || "http://localhost:8000";

function MyApp({ Component, pageProps }: AppProps): JSX.Element {
  return (
    <AuthProvider>
      <Component {...pageProps} />
    </AuthProvider>
  );
}
export default MyApp;
