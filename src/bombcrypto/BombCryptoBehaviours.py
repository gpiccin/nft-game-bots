from src.modules.Behaviours import Click, Information


class ConnectWalletClick(Click):
    def __init__(self, rectangle):
        super().__init__(rectangle)


class OkErrorClick(Click):
    def __init__(self, rectangle):
        super().__init__(rectangle)


class OkClick(Click):
    def __init__(self, rectangle):
        super().__init__(rectangle)


class SignOnMetamaskClick(Click):
    def __init__(self, rectangle):
        super().__init__(rectangle)


class CloseClick(Click):
    def __init__(self, rectangle):
        super().__init__(rectangle)


class SendAllHeroesToWorkClick(Click):
    def __init__(self, rectangle):
        super().__init__(rectangle)


class SendHeroToWorkClick(Click):
    def __init__(self, rectangle):
        super().__init__(rectangle)


class RestHeroClick(Click):
    def __init__(self, rectangle):
        super().__init__(rectangle)


class BackClick(Click):
    def __init__(self, rectangle):
        super().__init__(rectangle)


class TreasureHuntClick(Click):
    def __init__(self, rectangle):
        super().__init__(rectangle)


class RestAllHeroesClick(Click):
    def __init__(self, rectangle):
        super().__init__(rectangle)


class GoToHeroesClick(Click):
    def __init__(self, rectangle):
        super().__init__(rectangle)


class SlideUpToGoHeroesClick(Click):
    def __init__(self, rectangle):
        super().__init__(rectangle)


class SlideDownToGoHeroesClick(Click):
    def __init__(self, rectangle):
        super().__init__(rectangle)


class GreenBarClick(Information):
    def __init__(self, rectangle):
        super().__init__(rectangle)


class RedBarClick(Information):
    def __init__(self, rectangle):
        super().__init__(rectangle)


class FullBarClick(Information):
    def __init__(self, rectangle):
        super().__init__(rectangle)


class HeroLocalizationBarClick(Information):
    def __init__(self, rectangle):
        super().__init__(rectangle)