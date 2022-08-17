import React, { useState, useContext } from "react";
import AuthContext from "../../contexts/auth";

export const LoginBox = (): JSX.Element => {
  const [userData, setUserData] = useState({
    username: "",
    password: "",
    error: "",
  });

  const { loginUser } = useContext(AuthContext);

  async function handleSubmit(event: React.SyntheticEvent) {
    event.preventDefault();
    setUserData({ ...userData, error: "" });

    const username = userData.username;
    const password = userData.password;

    try {
      await loginUser(username, password);
    } catch (error) {
      console.error(error);
      let errorMessage = "Login failed";
      if (error instanceof Error) {
        errorMessage = error.message;
      }
      setUserData({ ...userData, error: errorMessage });
    }
  }
  return (
    <div className="login flex-3">
      <form onSubmit={handleSubmit} className="flex">
        <div className="flex-1 flex mx-1">
          {/*<label htmlFor="username">Username</label>*/}

          <input
            type="text"
            id="username"
            name="username"
            className="p-2 border border-gray-300 outline-none focus:border-gray-400 text-black"
            placeholder="Username"
            value={userData.username}
            onChange={(event) => setUserData(Object.assign({}, userData, { username: event.target.value }))}
          />
        </div>
        <div className="flex-2 flex mx-1">
          {/* <label htmlFor="password">Password</label> */}
          <input
            type="password"
            id="password"
            name="password"
            className="p-2 border border-gray-300 outline-none focus:border-gray-400 text-black"
            placeholder="Password"
            value={userData.password}
            onChange={(event) => setUserData(Object.assign({}, userData, { password: event.target.value }))}
          />
        </div>
        <button
          className="flex-3 relative items-center justify-center bg-blue-400 p-2 ml-1 hover:bg-blue-800"
          type="submit"
        >
          Login
        </button>

        {userData.error && <p className="error">Error: {userData.error}</p>}
      </form>
    </div>
  );
};
