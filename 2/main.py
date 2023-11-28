import pandas as pd


class HorrorMoviesProcessor:
    """Класс для обработки данных о хоррор фильмах."""

    def __init__(self, csv_path: str) -> None:
        """
        Конструктор класса.

        Args:
            csv_path (str): Путь к CSV-файлу
        """
        self.df = pd.read_csv(csv_path)

    def _delete_missing_rows(self) -> None:
        """Удаляет строки с недостающими данными."""
        self.df.dropna(inplace=True)

    def _filter_data(self) -> None:
        """Фильтрует данные. Оставляет только релизы и фильмы с четными id."""
        self.df = self.df[(self.df["id"] % 2 == 0) & (self.df["status"] == "Released")]

    def _expand_genres(self) -> None:
        """
        Разделяет жанры на отдельные столбцы.

        Создает DataFrame с разделенными жанрами
        """
        self.df_genres = self.df["genre_names"].str.split(
            ", ",
            expand=True,
        )

    def _convert_revenue_to_numeric(self) -> None:
        """Преобразование данных в столбце 'revenue' в числовой формат."""
        self.df["revenue"] = pd.to_numeric(
            self.df["revenue"],
            errors="coerce",
        )

    def _merge_dataframes(self) -> None:
        """Соединяет два DataFrame (self.df и self.df_genres) в один по индексам."""
        self.df = self.df_genres.merge(
            self.df,
            left_index=True,
            right_index=True,
            suffixes=(
                "_genre",
                "",
            ),
        )

    def _melt_dataframe(self) -> None:
        """Преобразует DataFrame, чтобы каждая строка представляла собой отдельный жанр."""
        self.df = self.df.melt(
            id_vars=self.df.columns.difference(
                self.df_genres.columns,
            ),
            value_name="genre",
        )

    def process_horror_movies(self) -> None:
        """Обрабатывает данные о хоррор фильмах."""
        self._delete_missing_rows()
        self._filter_data()
        self._expand_genres()
        self._convert_revenue_to_numeric()
        self._merge_dataframes()
        self._melt_dataframe()

    def get_genre_revenue_sum(self) -> pd.DataFrame:
        """
        Возвращает сумму доходов для каждого жанра.

        Returns:
            pd.DataFrame: Сумма доходов для каждого жанра
        """
        return self.df.groupby("genre")["revenue"].sum().reset_index(name="total_amount")

    def calculate_vote_budget_ratio(self) -> pd.DataFrame:
        """
        Вычисляет отношение средней оценки к средней стоимости для каждого жанра.

        Returns:
            pd.DataFrame: Отношение средней оценки к средней стоимости для каждого жанра
        """
        genre_vote_budget_ratio = (
            self.df.groupby("genre")
            .apply(
                lambda group: group["vote_average"].mean() / group["budget"].mean() if group["budget"].mean() > 0 else 0
            )
            .reset_index(name="vote_budget_ratio")
        )
        return genre_vote_budget_ratio


def main() -> None:
    """Основная функция."""
    processor = HorrorMoviesProcessor("horror_movies.csv")
    processor.process_horror_movies()
    genre_revenue_sum = processor.get_genre_revenue_sum()
    print(genre_revenue_sum)
    genre_vote_budget_ratio = processor.calculate_vote_budget_ratio()
    print(genre_vote_budget_ratio)


if __name__ == "__main__":
    main()
