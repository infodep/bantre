import React, { ReactNode } from "react";
import { Footer } from "./Footer";
import { Header } from "./Header";

interface Props {
  children: ReactNode;
}

export const Layout = ({ children }: Props): JSX.Element => {
  return (
    <>
      <div className="flex flex-col h-screen">
        <Header />
        <div className="container mx-auto px-4 flex-grow">{children}</div>
        <Footer />
      </div>
    </>
  );
};
