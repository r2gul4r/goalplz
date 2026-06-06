type ProductCardProps = {
  title: string;
  price: string;
  imageUrl: string;
  badge?: string;
};

export function ProductCard({ title, price, imageUrl, badge }: ProductCardProps) {
  return (
    <article className="product-card">
      <img className="product-card__image" src={imageUrl} alt="" />
      <div className="product-card__body">
        {badge ? <span className="product-card__badge">{badge}</span> : null}
        <h3>{title}</h3>
        <p>{price}</p>
        <button type="button">Add to cart</button>
      </div>
    </article>
  );
}
