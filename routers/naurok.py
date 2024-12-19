from time import sleep

from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

from selenium import webdriver
from selenium.webdriver.common.by import By

router = Router()


@router.message(
    Command(
        commands='naurok'
    )
)
async def naurok(message: Message):
    code = str(message.text).split()[1]

    if 'https://' in code or 'naurok.com' in code:
        code = code.split('=')[-1]
    else:
        None

    await message.answer(
        naurok_solver(code)
    )


def replace_answer(answer: str) -> str:
    return answer\
        .replace('&nbsp', ' ')\
        .replace('<sup>2</sup>', '^2')\
        .replace('<sup>3</sup>', '^3')\
        .replace(' ;', '')


def naurok_solver(code: str) -> str:
    try:
        driver = webdriver.Firefox()
        driver.get('https://naurok.com.ua/test/join')

        code_field = driver.find_element(
            By.ID,
            'joinform-gamecode'
        )
        code_field.clear()
        code_field.send_keys(code)

        name_field = driver.find_element(
            By.ID,
            'joinform-name'
        )
        name_field.clear()
        name_field.send_keys('Error connect: 404')

        sleep(1)

        driver.find_element(
            By.TAG_NAME,
            'button'
        ).click()

        sleep(3)

        test_variants = driver.find_element(
            By.XPATH,
            "//div[contains(@class, 'test-options-grid')]"
        )
        test_variants.find_element(
            By.TAG_NAME,
            'div'
        ).click()

        sleep(5)

        driver.find_element(
            By.CLASS_NAME,
            'endSessionButton'
        ).click()

        sleep(7)

        quest_div = driver.find_element(
            By.CSS_SELECTOR,
            'div.homework-stats'
        )

        quest_blocks = quest_div.find_elements(
            By.CLASS_NAME,
            'homework-stat-options'
        )

        correct_answers = []

        for i in quest_blocks:
            answers = i.find_elements(
                By.CLASS_NAME,
                'homework-stat-option-line'
            )
            correct_answer_block = [
                i for i in answers if 'correct' in i.get_attribute('outerHTML')
            ][0]

            num = correct_answer_block.find_element(
                By.CSS_SELECTOR,
                'span'
            ).get_attribute('innerHTML')

            correct_answer = correct_answer_block.find_element(
                By.CSS_SELECTOR,
                'p'
            ).get_attribute('innerHTML')

            correct_answers.append([num, replace_answer(correct_answer)])

        answer_text = ''

        for num, i in enumerate(correct_answers, start=1):
            answer_text += f'{num}: {i[0]}) {i[1]}\n'

        return replace_answer(answer_text)
    except Exception as ex:
        print(ex)
    finally:
        driver.quit()
