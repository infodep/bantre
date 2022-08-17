import { Article } from "../../interfaces/Article";

interface Props {
  article: Article;
}

export const ArticleBox = ({ article }: Props): JSX.Element => {
  return (
    <form className="article">
      <label htmlFor="title"></label>
      <input type="text" id="title" name="title" value={article.title}></input>
    </form>
  );
};

ArticleBox.defaultProps = {
  article: {
    title: "",
    text: "",
    text_source: "",
    image: 0,
  },
};
