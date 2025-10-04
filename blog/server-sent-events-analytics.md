# Server-Sent Events (SSE) for Live Analytics Feeds

## Introduction

Real-time analytics are essential for modern web applications, especially dashboards and monitoring tools. Server-Sent Events (SSE) provide a simple way to push live updates from the server to the browser, making them ideal for streaming analytics data to the UI.

## What are Server-Sent Events?

Server-Sent Events (SSE) is a browser API that allows servers to push text-based event data to clients over HTTP. Unlike WebSockets, SSE is unidirectional (server to client) and uses a simple event stream format.

- **Protocol:** HTTP
- **Direction:** Server → Client
- **Format:** Text/event-stream

## How SSE Works

1. The client (browser) opens a connection to the server using JavaScript's `EventSource` API.
2. The server responds with a stream of events, each formatted as text.
3. The browser receives and processes events in real time.

## Example: Live Analytics Feed

### Backend (Node.js Example)

```js
const http = require("http");

http
  .createServer((req, res) => {
    if (req.url === "/events") {
      res.writeHead(200, {
        "Content-Type": "text/event-stream",
        "Cache-Control": "no-cache",
        Connection: "keep-alive",
      });
      setInterval(() => {
        const data = JSON.stringify({
          users: Math.floor(Math.random() * 100),
          sales: Math.floor(Math.random() * 50),
        });
        res.write(`data: ${data}\n\n`);
      }, 2000);
    } else {
      res.writeHead(404);
      res.end();
    }
  })
  .listen(3000);
```

### Frontend (HTML + JS)

```html
<div id="analytics"></div>
<script>
  const analyticsDiv = document.getElementById("analytics");
  const source = new EventSource("/events");
  source.onmessage = function (event) {
    const data = JSON.parse(event.data);
    analyticsDiv.innerHTML = `Users: ${data.users}, Sales: ${data.sales}`;
  };
</script>
```

## Use Cases

- Real-time dashboards
- Live notifications
- Monitoring systems
- Stock tickers

## Best Practices

- Use SSE for simple, unidirectional data streams
- For bidirectional communication, consider WebSockets
- Handle reconnections gracefully in the client
- Secure your endpoints and validate data

## Conclusion

SSE is a powerful tool for streaming live analytics to your UI with minimal setup. It works well for dashboards and monitoring tools where real-time updates are crucial.

---

_Written by recscse, August 2025_
