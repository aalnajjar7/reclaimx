module.exports = async (req, res) => {
  if (req.method !== "POST") {
    return res.status(200).send("ok");
  }

  const BOT_TOKEN = "8681635672:AAGi-Q9LAw6U-YyrF71uOd1bI20hnX4Sa_Y";
  const WEBSITE_URL = "https://reclaimx.site.je/";

  const update = req.body;

  if (update.message && update.message.chat && update.message.chat.type === "private") {
    const chatId = update.message.chat.id;
    const firstName = update.message.chat.first_name || "صديقي";

    const welcome = "🎉 أهلاً بيك يا " + firstName + "!\n\n" +
      "أنا ReclaimX — منصة الأمن السيبراني والبرمجة 🛡️\n\n" +
      "📍 كل اللي تحتاجه هنا:\n" +
      "🔗 " + WEBSITE_URL + "\n\n" +
      "✨ دورات احترافية\n" +
      "🤖 اشتراكات الذكاء الاصطناعي\n" +
      "📱 خدمات السوشيال ميديا\n" +
      "🔒 استشارات أمنية\n\n" +
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