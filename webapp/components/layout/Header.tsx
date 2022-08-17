import Link from "next/link";
import Image from "next/image";
import { UserOrLogin } from "../user/UserOrLogin";
import logo from "../../assets/images/logo.svg";

export const Header = (): JSX.Element => {
  return (
    <div className="w-screen bg-gray-800">
      <div className="container mx-auto px-4">
        <nav className=" text-white items-center flex">
          <div className="my-2 mr-auto">
            <Image src={logo} alt="Timini" width={224} height={75} />
          </div>
          <Link href="/">
            <a>
              <div className="relative flex-1 items-center justify-center bg-blue-400 p-2 mx-1 hover:bg-blue-800 ">
                Home
              </div>
            </a>
          </Link>
          <Link href="/articles">
            <a>
              <div className="relative flex-2 items-center justify-center bg-blue-400 p-2 mx-1 hover:bg-blue-800">
                Articles
              </div>
            </a>
          </Link>
          <UserOrLogin />
        </nav>
      </div>
    </div>
  );
};
