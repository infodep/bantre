import { User } from "../../interfaces/User";
import { Error } from "../../interfaces/Error";
import useGet from "./useGet";

interface ReturnType {
  user: User | undefined;
  isLoading: boolean;
  isError: Error | undefined;
}

export default function useUser(id: number): ReturnType {
  const { data, error } = useGet<User, Error>(`/v1/user/${id}`);

  return {
    user: data,
    isLoading: !error && !data,
    isError: error,
  };
}
