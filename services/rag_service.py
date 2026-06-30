from pathlib import Path

from config import Config
from utils.logger import llm_logger


class RagService:
  def __init__(self, config: Config) -> None:
    self._docs_dir = Path(config.DOCS_DIR)

  def count_documents(self) -> int:
    if not self._docs_dir.exists():
      return 0
    return len(list(self._docs_dir.glob("*.md")) + list(self._docs_dir.glob("*.txt")))

  def search(self, question: str, limit: int = 3) -> list[str]:
    if not self._docs_dir.exists():
      return []

    question_tokens = {token for token in question.lower().split() if len(token) > 1}
    scored: list[tuple[int, str, str]] = []

    for path in sorted(self._docs_dir.glob("*")):
      if path.suffix.lower() not in {".md", ".txt"}:
        continue
      content = path.read_text(encoding="utf-8")
      content_lower = content.lower()
      score = sum(1 for token in question_tokens if token in content_lower)
      if score > 0:
        scored.append((score, path.name, content))

    scored.sort(key=lambda item: item[0], reverse=True)
    return [f"{name}: {body[:200].strip()}" for _, name, body in scored[:limit]]

  def load_all_snippets(self) -> list[str]:
    if not self._docs_dir.exists():
      return []

    snippets: list[str] = []
    for path in sorted(self._docs_dir.glob("*")):
      if path.suffix.lower() not in {".md", ".txt"}:
        continue
      snippets.append(f"[{path.name}] {path.read_text(encoding='utf-8')[:500].strip()}")
    return snippets
