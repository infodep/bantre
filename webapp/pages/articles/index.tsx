import axios from "axios";
import { NextPage, GetServerSideProps } from "next";
import { ArticleBox } from "../../components/article/ArticleBox";
import { Layout } from "../../components/layout/Layout";
import useGet from "../../helpers/hooks/useGet";
import { Article } from "../../interfaces/Article";

interface ArticleProps {
  articles: Article[];
}

const Articles: NextPage<ArticleProps> = ({ articles }) => {
  const { data } = useGet<Article[]>("/v1/article/", { fallbackData: articles });
  return (
    <Layout>
      {data?.map((article, index) => (
        <ArticleBox article={article} key={index} />
      ))}
    </Layout>
  );
};

export const getServerSideProps: GetServerSideProps = async () => {
  const data = await axios.get("/v1/article/").then((res) => res.data);

  return {
    props: {
      articles: data,
    },
  };
};

export default Articles;
