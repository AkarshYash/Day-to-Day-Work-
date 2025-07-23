// main.cpp
#include <QApplication>
#include <QtWidgets>
#include <QtNetwork>
#include <QJsonDocument>
#include <QJsonObject>
#include <QTextEdit>

class ChatBotWidget : public QWidget {
    Q_OBJECT
public:
    ChatBotWidget(QWidget* parent = nullptr) : QWidget(parent) {
        setWindowTitle("Offline Code ChatBot (CodeLlama + Qt)");

        userInput = new QTextEdit();
        userInput->setPlaceholderText("Ask your coding question here...");
        userInput->setFixedHeight(100);

        sendButton = new QPushButton("Send");
        output = new QTextEdit();
        output->setReadOnly(true);

        QVBoxLayout* layout = new QVBoxLayout();
        layout->addWidget(new QLabel("🤖 Ask Offline Code ChatBot:"));
        layout->addWidget(userInput);
        layout->addWidget(sendButton);
        layout->addWidget(new QLabel("💡 Response:"));
        layout->addWidget(output);
        setLayout(layout);

        manager = new QNetworkAccessManager(this);

        connect(sendButton, &QPushButton::clicked, this, &ChatBotWidget::sendPrompt);
    }

private slots:
    void sendPrompt() {
        QString prompt = userInput->toPlainText().trimmed();
        if (prompt.isEmpty()) {
            QMessageBox::warning(this, "Oops!", "Please enter a prompt.");
            return;
        }

        output->setText("🕐 Thinking (offline)...");

        // Prepare JSON payload
        QJsonObject json;
        json["model"] = "codellama:7b-instruct";
        json["prompt"] = prompt;
        json["stream"] = false;

        QNetworkRequest request(QUrl("http://localhost:11434/api/generate"));
        request.setHeader(QNetworkRequest::ContentTypeHeader, "application/json");

        QNetworkReply* reply = manager->post(request, QJsonDocument(json).toJson());
        connect(reply, &QNetworkReply::finished, this, [=]() {
            if (reply->error() != QNetworkReply::NoError) {
                output->setText("❌ Error: " + reply->errorString());
            } else {
                QJsonDocument doc = QJsonDocument::fromJson(reply->readAll());
                if (doc.isObject() && doc.object().contains("response")) {
                    QString result = doc.object()["response"].toString();
                    output->setTextFormat(Qt::PlainText);
                    output->setText(result);
                } else {
                    output->setText("❓ Unexpected response.");
                }
            }
            reply->deleteLater();
        });
    }

private:
    QTextEdit* userInput;
    QTextEdit* output;
    QPushButton* sendButton;
    QNetworkAccessManager* manager;
};

int main(int argc, char* argv[]) {
    QApplication app(argc, argv);
    ChatBotWidget window;
    window.resize(600, 500);
    window.show();
    return app.exec();
}

#include "main.moc"
