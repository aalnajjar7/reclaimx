module.exports = async (req, res) => {
  if (req.method !== "POST") {
    return res.status(200).send("ok");
  }

  const BOT_TOKEN = "8996407648:AAE4zGF-CAadrCkLFE_p_K9yWuWOKv2pALE";
  const WEBSITE_URL = "https://reclaimx.site.je/";
  const INSTAGRAM_URL = "https://www.instagram.com/reclaimx.me";
  const TELEGRAM_CONTACT = "@reclaimxx";

  const update = req.body;

  if (update.message && update.message.chat && update.message.chat.type === "private") {
    const chatId = update.message.chat.id;
    const firstName = update.message.chat.first_name || "صديقي";

    const welcome = "🎉 أهلاً بك يا " + firstName + "!\n\n" +
      "أنا بوت ReclaimX — بوابتك إلى عالم الأمن السيبراني والبرمجة 🛡️\n\n" +
      "━━━━━━━━━━━━━━\n" +
      "🎯 ماذا نقدّم؟\n\n" +
      "📚 دورات احترافية\n" +
      "🤖 اشتراكات الذكاء الاصطناعي\n" +
      "📱 خدمات السوشيال ميديا\n" +
      "💻 تطوير الويب والتصميم\n" +
      "🔒 استشارات أمنية\n" +
      "━━━━━━━━━━━━━━\n\n" +
      "🌐 اكتشف كل ما تحتاجه على موقعنا:\n" +
      "🔗 " + WEBSITE_URL + "\n\n" +
      "📷 تابعنا على إنستقرام:\n" +
      "🔗 " + INSTAGRAM_URL + "\n\n" +
      "💬 لأي استفسار: " + TELEGRAM_CONTACT + "\n\n" +
      "ابدأ رحلتك الآن 🚀";

    const url = "https://api.telegram.org/bot" + BOT_TOKEN + "/sendMessage";

    try {
      await fetch(url, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          chat_id: chatId,
          text: welcome,
          parse_mode: "Markdown",
          disable_web_page_preview: false
        })
      });
    } catch (e) {
      console.error(e);
    }
  }

  res.status(200).send("ok");
};