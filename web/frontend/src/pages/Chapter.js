// 章节试炼页游页面：按知识章节闯关（六章 × 初窥/进阶/登峰三关）
import { api } from "../lib/api.js";
import { toast } from "../components/ui/Toast.js";

const CHAPTER_ICONS = {
  concepts: "fa-yin-yang",
  network: "fa-network-wired",
  storage: "fa-database",
  pod: "fa-cube",
  deployment: "fa-rocket",
  security: "fa-shield-alt",
};

const TIER_STARS = (n) => "★".repeat(n) + "☆".repeat(3 - n);

export class ChapterPage {
  constructor() {
    this.chapters = [];
    this.selected = null; // 当前章节
    this.session = null; // { category, tier, total, target }
    this.current = null; // 当前题目视图
    this.multi = new Set(); // 多选题已选字母
    this.lastResult = null; // 最后一题判答结果
  }

  async mount(container) {
    this.container = container;
    await this.loadChapters();
  }

  async loadChapters() {
    this.container.innerHTML = `<div class="p-6 text-muted-foreground">加载中...</div>`;
    try {
      const resp = await api.getChapters();
      this.chapters = resp.data;
      this.selected = null;
      this.session = null;
      this.current = null;
      this.renderList();
    } catch (e) {
      this.renderError(e.message);
    }
  }

  renderError(msg) {
    this.container.innerHTML = `
      <div class="p-6">
        <div class="rounded-lg border border-red-500/30 bg-red-500/10 p-4 text-red-400">
          <i class="fas fa-exclamation-triangle mr-2"></i>${msg}
        </div>
        <button id="chapter-retry" class="mt-4 rounded-lg bg-primary px-4 py-2 text-primary-foreground">重试</button>
      </div>`;
    document.getElementById("chapter-retry")?.addEventListener("click", () => this.loadChapters());
  }

  // ---------- 章节列表 ----------
  renderList() {
    const cards = this.chapters
      .map((ch) => {
        const tiers = ch.tiers
          .map((t) => {
            let cls = "border-border text-muted-foreground";
            if (t.passed) cls = "border-green-500/40 bg-green-500/10 text-green-400";
            else if (t.unlocked) cls = "border-yellow-500/40 bg-yellow-500/10 text-yellow-400";
            const label = t.passed ? `${t.name} ${TIER_STARS(t.stars)}` : t.unlocked ? t.name : `${t.name} 🔒`;
            return `<span class="rounded-full border px-2.5 py-0.5 text-xs ${cls}">${label}</span>`;
          })
          .join("");
        return `
        <button data-chapter="${ch.category}" class="chapter-card game-card text-left">
          <div class="flex items-center justify-between">
            <div class="flex items-center gap-3">
              <div class="flex h-10 w-10 items-center justify-center rounded-lg bg-primary/10">
                <i class="fas ${CHAPTER_ICONS[ch.category] || "fa-book"} text-primary"></i>
              </div>
              <div>
                <div class="font-semibold">${ch.name}</div>
                <div class="text-xs text-muted-foreground">已通关 ${ch.total_passed}/3 关</div>
              </div>
            </div>
            <i class="fas fa-chevron-right text-muted-foreground"></i>
          </div>
          <div class="mt-3 flex flex-wrap gap-2">${tiers}</div>
        </button>`;
      })
      .join("");

    this.container.innerHTML = `
      <div class="p-6">
        <div class="mb-6">
          <h2 class="text-2xl font-bold">🏯 章节试炼</h2>
          <p class="mt-1 text-sm text-muted-foreground">
            六大知识章节 × 三关难度（初窥 1-2★ / 进阶 3★ / 登峰 4-5★），每关 10 题答对 7 题通关，首通奖励经验
          </p>
        </div>
        <div class="grid gap-4 md:grid-cols-2 xl:grid-cols-3">${cards}</div>
      </div>`;

    this.container.querySelectorAll("[data-chapter]").forEach((btn) => {
      btn.addEventListener("click", () => {
        this.selected = this.chapters.find((c) => c.category === btn.dataset.chapter);
        this.renderTiers();
      });
    });
  }

  // ---------- 关卡选择 ----------
  renderTiers() {
    const ch = this.selected;
    const rows = ch.tiers
      .map((t) => {
        const disabled = !t.unlocked;
        const status = t.passed
          ? `<span class="text-green-400">已通关 ${TIER_STARS(t.stars)}（最佳答对 ${t.best_correct}/${t.question_count}）</span>`
          : t.unlocked
            ? `<span class="text-yellow-400">可挑战 · 难度${t.difficulty_label} · ${t.question_count}题</span>`
            : `<span class="text-muted-foreground">未解锁：先通过上一关</span>`;
        return `
        <button data-tier="${t.tier}" ${disabled ? "disabled" : ""}
          class="game-card w-full text-left ${disabled ? "cursor-not-allowed opacity-40" : "hover:border-primary/50"}">
          <div class="flex items-center justify-between">
            <div class="font-medium">第${t.tier}关 · ${t.name}</div>
            ${status}
          </div>
        </button>`;
      })
      .join("");

    this.container.innerHTML = `
      <div class="p-6">
        <button id="chapter-back" class="mb-4 text-sm text-muted-foreground hover:text-foreground">
          <i class="fas fa-arrow-left mr-1"></i>返回章节列表
        </button>
        <h2 class="text-2xl font-bold">
          <i class="fas ${CHAPTER_ICONS[ch.category] || "fa-book"} text-primary mr-2"></i>${ch.name} · 章节试炼
        </h2>
        <p class="mt-1 text-sm text-muted-foreground">通关线为答对题数的 70%，星级按正确率评定（≥90% 三星 / ≥80% 两星）</p>
        <div class="mt-6 space-y-3">${rows}</div>
      </div>`;

    document.getElementById("chapter-back")?.addEventListener("click", () => this.renderList());
    this.container.querySelectorAll("[data-tier]:not([disabled])").forEach((btn) => {
      btn.addEventListener("click", () => this.startTier(parseInt(btn.dataset.tier, 10)));
    });
  }

  async startTier(tier) {
    try {
      const resp = await api.startChapterTier(this.selected.category, tier);
      this.session = { category: this.selected.category, tier, ...resp.data };
      await this.fetchCurrent();
    } catch (e) {
      toast.error("无法开始", e.message);
    }
  }

  // ---------- 答题 ----------
  async fetchCurrent() {
    try {
      const resp = await api.getCurrentChapterQuestion();
      this.current = resp.data;
      this.multi = new Set();
      this.lastResult = null;
      this.renderPlay();
    } catch {
      this.renderTiers(); // 会话不存在（理论上不应发生）
    }
  }

  renderPlay() {
    const q = this.current;
    const shown = Math.min(q.correct_so_far, q.target);
    const stars = "★".repeat(q.difficulty);
    const optsHtml = (q.options || [])
      .map(
        (o) => `
        <button data-opt="${o.slice(0, 1)}" class="game-card option-btn w-full text-left hover:border-primary/60">
          ${o}
        </button>`
      )
      .join("");

    let answerArea = "";
    if (this.lastResult) {
      const ok = this.lastResult.correct;
      answerArea = `
        <div class="mt-5 rounded-lg border p-4 ${ok ? "border-green-500/40 bg-green-500/10" : "border-red-500/40 bg-red-500/10"}">
          <div class="whitespace-pre-line ${ok ? "text-green-400" : "text-red-400"}">${this.escape(this.lastResult.feedback)}</div>
        </div>
        <div class="mt-4 flex gap-3">
          <button id="chapter-next" class="rounded-lg bg-primary px-5 py-2 font-medium text-primary-foreground">
            ${this.lastResult.finished ? "查看结算" : "下一题"}
          </button>
          <button id="chapter-quit" class="rounded-lg border border-border px-4 py-2 text-muted-foreground hover:bg-accent">放弃</button>
        </div>`;
    } else if (q.type === "multiple_choice") {
      answerArea = `
        <div class="mt-4"><div class="text-xs text-muted-foreground">已选：<span id="multi-shown">未选择</span></div></div>
        <div class="mt-4 flex gap-3">
          <button id="multi-submit" class="rounded-lg bg-primary px-5 py-2 font-medium text-primary-foreground">提交答案</button>
          <button id="chapter-quit" class="rounded-lg border border-border px-4 py-2 text-muted-foreground hover:bg-accent">放弃</button>
        </div>`;
    } else if (q.type === "true_false") {
      answerArea = `
        <div class="mt-4 flex gap-3">
          <button data-opt="T" class="option-btn rounded-lg bg-primary px-6 py-2 font-medium text-primary-foreground">对</button>
          <button data-opt="F" class="option-btn rounded-lg border border-border px-6 py-2 font-medium hover:bg-accent">错</button>
          <button id="chapter-quit" class="ml-auto rounded-lg border border-border px-4 py-2 text-muted-foreground hover:bg-accent">放弃</button>
        </div>`;
    } else if (!q.options) {
      answerArea = `
        <div class="mt-4 flex gap-3">
          <input id="chapter-input" class="flex-1 rounded-lg border border-border bg-background px-4 py-2 outline-none focus:border-primary" placeholder="输入答案" />
          <button id="text-submit" class="rounded-lg bg-primary px-5 py-2 font-medium text-primary-foreground">提交</button>
          <button id="chapter-quit" class="rounded-lg border border-border px-4 py-2 text-muted-foreground hover:bg-accent">放弃</button>
        </div>`;
    } else {
      answerArea = `<button id="chapter-quit" class="mt-4 rounded-lg border border-border px-4 py-2 text-muted-foreground hover:bg-accent">放弃</button>`;
    }

    this.container.innerHTML = `
      <div class="mx-auto max-w-3xl p-6">
        <button id="chapter-home" class="mb-4 text-sm text-muted-foreground hover:text-foreground">
          <i class="fas fa-arrow-left mr-1"></i>${this.session.category_name || "章节"}试炼
        </button>
        <div class="flex items-center justify-between text-sm text-muted-foreground">
          <span><span class="font-bold text-foreground">第 ${q.index}/${q.total} 题</span>　答对 ${shown}/${q.target}</span>
          <span>难度 <span class="text-primary">${stars}</span></span>
        </div>
        <div class="game-card mt-3">
          <div class="whitespace-pre-line font-medium">${this.escape(q.question)}</div>
          ${q.options ? `<div class="mt-4 space-y-2">${optsHtml}</div>` : ""}
        </div>
        ${answerArea}
      </div>`;

    this.bindPlayEvents();
  }

  bindPlayEvents() {
    const q = this.current;

    document.getElementById("chapter-home")?.addEventListener("click", () => this.loadChapters());
    document.getElementById("chapter-quit")?.addEventListener("click", () => this.loadChapters());
    document.getElementById("chapter-next")?.addEventListener("click", async () => {
      if (this.lastResult?.finished) {
        this.renderSettle(this.lastResult);
      } else {
        await this.fetchCurrent();
      }
    });

    if (this.lastResult) return; // 已判答，无输入交互

    // 单选/判断：点击即作答
    this.container.querySelectorAll(".option-btn[data-opt]").forEach((btn) => {
      btn.addEventListener("click", async () => {
        const letter = btn.dataset.opt;
        if (q.type === "true_false") {
          await this.submit(letter === "T" ? "True" : "False");
        } else if (q.type === "multiple_choice") {
          this.multi.has(letter) ? this.multi.delete(letter) : this.multi.add(letter);
          this.refreshMulti();
        } else {
          await this.submit(letter);
        }
      });
    });

    if (q.type === "multiple_choice") {
      document.getElementById("multi-submit")?.addEventListener("click", async () => {
        if (!this.multi.size) return toast.info("提示", "请先选择选项");
        await this.submit([...this.multi].sort());
      });
    }

    const input = document.getElementById("chapter-input");
    if (input) {
      document.getElementById("text-submit")?.addEventListener("click", async () => {
        if (!input.value.trim()) return toast.info("提示", "请输入答案");
        await this.submit(input.value.trim());
      });
      input.addEventListener("keydown", (e) => {
        if (e.key === "Enter") document.getElementById("text-submit")?.click();
      });
      input.focus();
    }
  }

  refreshMulti() {
    const shown = document.getElementById("multi-shown");
    if (shown) shown.textContent = this.multi.size ? [...this.multi].sort().join(", ") : "未选择";
  }

  async submit(answer) {
    try {
      const resp = await api.answerChapter(answer);
      this.lastResult = resp.data;
      this.renderPlay();
    } catch (e) {
      toast.error("判答失败", e.message);
    }
  }

  // ---------- 结算 ----------
  renderSettle(r) {
    const passed = r.passed;
    const body = passed
      ? `<div class="text-3xl text-yellow-400">${TIER_STARS(r.stars)}</div>
         ${r.first_clear && r.exp_gained ? `<div class="mt-2 text-sm text-green-400"><i class="fas fa-gift mr-1"></i>首通奖励 +${r.exp_gained} 经验值</div>` : ""}`
      : `<div class="text-muted-foreground">离通关线还差一点，再练练吧！</div>`;

    this.container.innerHTML = `
      <div class="mx-auto max-w-3xl p-6">
        <div class="game-card mx-auto mt-10 max-w-md text-center">
          <div class="text-5xl">${passed ? "🎉" : "💪"}</div>
          <h3 class="mt-3 text-2xl font-bold ${passed ? "text-green-400" : "text-red-400"}">
            ${passed ? "关卡通过" : "挑战失败"}
          </h3>
          <p class="mt-1 text-muted-foreground">${r.category_name} 第${r.tier}关</p>
          <p class="mt-4">答对 <span class="font-bold">${r.correct_so_far}</span>/${r.answered_count}（通关线 ${r.target}）</p>
          <div class="mt-3">${body}</div>
          <div class="mt-6 flex justify-center gap-3">
            <button id="settle-retry" class="rounded-lg bg-primary px-5 py-2 font-medium text-primary-foreground">再来一次</button>
            <button id="settle-back" class="rounded-lg border border-border px-5 py-2 hover:bg-accent">返回章节</button>
          </div>
        </div>
      </div>`;

    document.getElementById("settle-retry")?.addEventListener("click", () => this.startTier(r.tier));
    document.getElementById("settle-back")?.addEventListener("click", () => this.loadChapters());
  }

  escape(text) {
    const div = document.createElement("div");
    div.textContent = String(text ?? "");
    return div.innerHTML;
  }
}
