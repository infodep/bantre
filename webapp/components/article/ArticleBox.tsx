import { Article } from "../../interfaces/Article";

interface Props {
  article: Article;
}

export const ArticleBox = ({ article }: Props): JSX.Element => {
  return (
    <div className="article" key={article.id}>
      <h1>{article.title}</h1>
      <p>
        {article.text}
        created by: {article.creator_id}
      </p>
    </div>
  );
};
