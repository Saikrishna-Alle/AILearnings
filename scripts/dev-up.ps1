param(
  [switch]$Down
)

if ($Down) {
  docker compose down
} else {
  docker compose up --build
}
