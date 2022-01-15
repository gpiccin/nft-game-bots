from src.modules.Behaviours import Click, Behaviour, Information


class ConnectWallet(Click):
    def __init__(self, rectangle):
        super().__init__(rectangle)


class OkError(Click):
    def __init__(self, rectangle):
        super().__init__(rectangle)


class Ok(Click):
    def __init__(self, rectangle):
        super().__init__(rectangle)


class SignOnMetamask(Click):
    def __init__(self, rectangle):
        super().__init__(rectangle)


class Close(Click):
    def __init__(self, rectangle):
        super().__init__(rectangle)


class SendAllHeroesToWork(Click):
    def __init__(self, rectangle):
        super().__init__(rectangle)


class SendHeroToWork(Click):
    def __init__(self, rectangle):
        super().__init__(rectangle)


class RestHero(Click):
    def __init__(self, rectangle):
        super().__init__(rectangle)


class Back(Click):
    def __init__(self, rectangle):
        super().__init__(rectangle)


class TreasureHunt(Click):
    def __init__(self, rectangle):
        super().__init__(rectangle)


class RestAllHeroes(Click):
    def __init__(self, rectangle):
        super().__init__(rectangle)


class GoToHeroes(Click):
    def __init__(self, rectangle):
        super().__init__(rectangle)


class SlideUpToGoHeroes(Click):
    def __init__(self, rectangle):
        super().__init__(rectangle)


class SlideDownToGoHeroes(Click):
    def __init__(self, rectangle):
        super().__init__(rectangle)


class GreenBar(Information):
    def __init__(self, rectangle):
        super().__init__(rectangle)


class RedBar(Information):
    def __init__(self, rectangle):
        super().__init__(rectangle)


class FullBar(Information):
    def __init__(self, rectangle):
        super().__init__(rectangle)


class HeroLocalizationBar(Information):
    def __init__(self, rectangle):
        super().__init__(rectangle)