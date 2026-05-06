from dataclasses import dataclass
from calendar import monthrange
from datetime import date
from typing import Optional
from db import get_connection

@dataclass
class PlatformReport:
    reportType: str
    reportTitle: str
    startDate: str
    endDate: str
    totalDonationsCollected: float
    totalUserLogins: int
    totalActiveFundraisingActivities: int
    totalCompletedActivities: int
    mostActiveCategory: Optional[str]

    @classmethod
    def generateDailyReport(cls, selectedDate: str) -> "PlatformReport":
        return cls.generateDailyReportInDateRange(
            reportType = "daily",
            reportTitle = f"Daily Report: {selectedDate}",
            startDate = selectedDate,
            endDate = selectedDate
        )

    @classmethod
    def generateWeeklyReport(cls, dateFrom: str, dateTo: str) -> "PlatformReport":
        return cls._generateReportInDateRange(
            reprotType = "weekly",
            reportTitle = f"Weekly Report ({dateFrom} to {dateTo})",
            startDate = dateFrom,
            endDate = dateTo
        )

    @classmethod
    def generateMonthlyReport(cls, selectedMonth: int, selectedYear: int) -> "PlatformReport":
        startDate = date(selectedYear, selectedMonth, 1).isoformat()
        endDate = date(selectedYear, selectedMonth, monthrange(selectedYear, selectedMonth)[1]).isoformat()

        return cls._generateReportForRange(
            reportType = "monthly",
            reportTitle = f"Monthly Report ({selectedYear} - {selectedMonth:02d})",
            startDate = startDate,
            endDate = endDate
        )

    @classmethod
    def _generateReportInDateRange(cls, reportType: str, reportTitle: str, startDate: str, endDate: str) -> "PlatformReport":
        connection = get_connection()
        donationsRow = connection.execute(
            """
            SELECT COALESCE(SUM(donation_amount), 0) AS total_donations
            FROM donation
            WHERE donation_date BETWEEN ? AND ?
            """,
            (startDate, endDate)
        ).fetchone()

        loginsRow = connection.execute()
