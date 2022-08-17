import { useContext } from "react";
import AuthContext from "../../contexts/auth";
import { LoginBox } from "./LoginBox";
import { UserBox } from "./UserBox";

export const UserOrLogin = (): JSX.Element => {
  const { user_id, logoutUser } = useContext(AuthContext);
  if (user_id) {
    return (
      <>
        <UserBox />
        <button onClick={logoutUser}>Logout</button>
      </>
    );
  } else {
    return <LoginBox />;
  }
};
