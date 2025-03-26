export async function load() {
    const res = await fetch('http://localhost:8000/api/orders');
    const orders = await res.json();
  
    return {
      orders
    };
  }
  