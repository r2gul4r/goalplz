type OrderLine = {
  id: string;
  label: string;
  quantity: number;
  unitPrice: number;
};

type OrderSummaryProps = {
  lines: OrderLine[];
  discount: number;
  shipping: number;
  tax: number;
};

export function OrderSummary(props: OrderSummaryProps) {
  const subtotal = props.lines.reduce((sum, line) => sum + line.quantity * line.unitPrice, 0);
  const total = subtotal - props.discount + props.shipping + props.tax;

  return (
    <aside className="order-summary">
      <h2>Order summary</h2>
      <div>
        {props.lines.map((line) => (
          <div key={line.id} className="order-summary__line">
            <span>{line.label}</span>
            <span>{line.quantity}</span>
            <span>{line.unitPrice}</span>
          </div>
        ))}
      </div>
      <div className="order-summary__totals">
        <div>
          <span>Subtotal</span>
          <strong>{subtotal}</strong>
        </div>
        <div>
          <span>Discount</span>
          <strong>{props.discount}</strong>
        </div>
        <div>
          <span>Shipping</span>
          <strong>{props.shipping}</strong>
        </div>
        <div>
          <span>Tax</span>
          <strong>{props.tax}</strong>
        </div>
        <div>
          <span>Total</span>
          <strong>{total}</strong>
        </div>
      </div>
    </aside>
  );
}
