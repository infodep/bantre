import axios from "axios";
import { NextPage, GetStaticProps, GetStaticPaths } from "next";
import { useRouter } from "next/router";
import { ArticleBox } from "../../components/article/ArticleBox";
import { Layout } from "../../components/layout/Layout";
import useGet from "../../helpers/hooks/useGet";
import { Article } from "../../interfaces/Article";

interface ArticleProps {
  article: Article;
}

const ViewArticle: NextPage<ArticleProps> = ({ article }) => {
  const router = useRouter();
  const { id } = router.query;
  const { data } = useGet<Article>(`/v1/article/${id}`, { fallbackData: article });
  return (
    <Layout>
      <ArticleBox article={data!} />
    </Layout>
  );
};

export const getStaticPaths: GetStaticPaths = async () => {
  // Call an external API endpoint to get posts
  const articles = await axios.get(`/v1/article/`).then((res) => res.data);

  // Get the paths we want to pre-render based on posts
  const paths = articles.map((article: Article) => ({
    params: { id: article.id.toString() },
  }));

  // We'll pre-render only these paths at build time.
  // { fallback: false } means other routes should 404.
  return { paths, fallback: false };
};

export const getStaticProps: GetStaticProps = async ({ params }) => {
  const data = params ? await axios.get(`/v1/article/${params.id}`).then((res) => res.data) : null;

  return {
    props: {
      article: data,
    },
  };
};

export default ViewArticle;
