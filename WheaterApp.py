import customtkinter as ctk
import requests
from datetime import datetime

ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")

class WeatherApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Прогноз Погоды")
        self.geometry("700x700")
        self.resizable(False, False)
        self.api_key = "ключ API"
        self.create_widgets()

    def create_widgets(self):
        title_label = ctk.CTkLabel(
            self,
            text="Прогноз Погоды",
            font=("Arial", 24, "bold")
        )
        title_label.pack(pady=20)

        input_frame = ctk.CTkFrame(self)
        input_frame.pack(fill="x", padx=20, pady=10)

        self.city_entry = ctk.CTkEntry(
            input_frame,
            placeholder_text="Введите название города, например: Москва",
            font=("Arial", 16),
            height=40
        )
        self.city_entry.pack(side="left", fill="x", expand=True, padx=(0, 10))
        self.city_entry.bind("<Return>", lambda e: self.get_weather())

        search_button = ctk.CTkButton(
            input_frame,
            text="Поиск",
            command=self.get_weather,
            width=100,
            height=40,
            fg_color="green",
            hover_color="darkgreen"
        )
        search_button.pack(side="right")

        self.weather_frame = ctk.CTkFrame(self, height=500)
        self.weather_frame.pack(fill="both", expand=True, padx=20, pady=20)

        self.result_label = ctk.CTkLabel(
            self.weather_frame,
            text="Для отображения прогноза погоды, введите название города!",
            font=("Arial", 14),
            text_color="gray"
        )
        self.result_label.pack(expand=True)

    def get_weather(self):
        city = self.city_entry.get().strip()
        if not city:
            self.show_error("Введите название города!!!")
            return

        try:
            # Запрос к Visual Crossing API
            url = f"https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline/{city}"
            params = {
                "key": self.api_key,
                "unitGroup": "metric",
                "lang": "ru",
                "include": "current,days"
            }

            response = requests.get(url, params=params)

            if response.status_code == 200:
                data = response.json()
                self.display_weather(data)
            elif response.status_code == 400:
                self.show_error("Город не найден!!!")
            else:
                self.show_error(f"Ошибка API: {response.status_code}")

        except requests.exceptions.ConnectionError:
            self.show_error("Нет подключения к интернету")
        except Exception as e:
            self.show_error("Ошибка запроса к серверу")

    def display_weather(self, data):
        for widget in self.weather_frame.winfo_children():
            widget.destroy()

        current = data["currentConditions"]
        address = data["resolvedAddress"]
        temp = current["temp"]
        feels_like = current.get("feelslike", temp)
        humidity = current["humidity"]
        pressure = current["pressure"]
        wind_speed = current["windspeed"]
        description = current["conditions"]

        icon = self.get_weather_icon(current["icon"])

        ctk.CTkLabel(
            self.weather_frame,
            text=f"{icon} {address}",
            font=("Arial", 18, "bold")
        ).pack(pady=(10, 5))

        ctk.CTkLabel(
            self.weather_frame,
            text=f"{temp}°C",
            font=("Arial", 36, "bold")
        ).pack(pady=5)

        ctk.CTkLabel(
            self.weather_frame,
            text=description,
            font=("Arial", 16)
        ).pack(pady=(0, 10))

        ctk.CTkLabel(
            self.weather_frame,
            text=f"Ощущается как: {feels_like}°C",
            font=("Arial", 14)
        ).pack(pady=2)

        details_frame = ctk.CTkFrame(self.weather_frame)
        details_frame.pack(fill="x")

        ctk.CTkLabel(
            details_frame,
            text=f"💧 Влажность: {humidity}%",
            font=("Arial", 14)
        ).pack(pady=2)

        ctk.CTkLabel(
            details_frame,
            text=f"📊 Давление: {pressure} гПа",
            font=("Arial", 14)
        ).pack(pady=2)

        ctk.CTkLabel(
            details_frame,
            text=f"💨 Ветер: {wind_speed} км/ч",
            font=("Arial", 14)
        ).pack(pady=2)

        if "days" in data and len(data["days"]) > 1:
            ctk.CTkLabel(
                self.weather_frame,
                text="📅 Прогноз на 5 дней",
                font=("Arial", 16, "bold")
            ).pack(pady=(15, 5))

            forecast_frame = ctk.CTkFrame(self.weather_frame)
            forecast_frame.pack(fill="x")

            # Показываем прогноз на 5 дней (кроме сегодня)
            for day_data in data["days"][1:6]:
                day_frame = ctk.CTkFrame(forecast_frame)
                day_frame.pack(fill="x")

                date = datetime.strptime(day_data["datetime"], "%Y-%m-%d")
                day_name = date.strftime("%a")
                temp_max = day_data["tempmax"]
                temp_min = day_data["tempmin"]
                icon = self.get_weather_icon(day_data["icon"])

                ctk.CTkLabel(
                    day_frame,
                    text=f"{day_name} {icon} {temp_max}°/{temp_min}°",
                    font=("Arial", 12)
                ).pack(pady=5)

        ctk.CTkLabel(
            self.weather_frame,
            text=f"Обновлено: {datetime.now().strftime('%d.%m.%Y %H:%M')}",
            font=("Arial", 10),
            text_color="gray"
        ).pack(pady=(10, 5))

    def get_weather_icon(self, icon_code):
        icons = {
            "clear-day": "☀️",
            "clear-night": "🌙",
            "partly-cloudy-day": "⛅",
            "partly-cloudy-night": "☁️",
            "cloudy": "☁️",
            "rain": "🌧️",
            "snow": "❄️",
            "sleet": "🌨️",
            "wind": "💨",
            "fog": "🌫️",
            "thunder-rain": "⛈️",
            "thunder-showers-day": "⛈️",
            "thunder-showers-night": "⛈️"
        }
        return icons.get(icon_code, "🌤️")

    def show_error(self, message):
        for widget in self.weather_frame.winfo_children():
            widget.destroy()

        ctk.CTkLabel(
            self.weather_frame,
            text=message,
            font=("Arial", 16),
            text_color="red"
        ).pack(expand=True)

if __name__ == "__main__":
    app = WeatherApp()
    app.mainloop()