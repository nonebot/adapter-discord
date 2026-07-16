from collections.abc import Sequence
from typing import TYPE_CHECKING, Annotated, Literal, overload
from typing_extensions import Unpack

from .read import AuditLog, AutoModerationAction, AutoModerationRule, TriggerMetadata
from .types import AuditLogEventType, AutoModerationRuleEventType, TriggerType
from .write import (
    CreateAutoModerationRuleParams,
    ModifyAutoModerationRuleParams,
)
from ...api.validation import (
    AtMostOne,
    Range,
    validate,
    validate_outbound_value,
)
from ...protocol import SnowflakeType
from ...transport.exchange import (
    REST_EXCHANGE,
    BotAuth,
    EmptyResponse,
    JsonBody,
    JsonResponse,
    RestCall,
)

if TYPE_CHECKING:
    from ...api.handle import AdapterProtocol
    from ...bot import Bot

NonSpamTriggerType = Literal[
    TriggerType.KEYWORD,
    TriggerType.KEYWORD_PRESET,
    TriggerType.MENTION_SPAM,
    TriggerType.MEMBER_PROFILE,
]


def _validate_auto_moderation_exemptions(
    *,
    exempt_roles: Sequence[SnowflakeType] | None,
    exempt_channels: Sequence[SnowflakeType] | None,
) -> None:
    if exempt_roles is not None and len(exempt_roles) > 20:  # noqa: PLR2004
        msg = "exempt_roles must be 20 items or fewer"
        raise ValueError(msg)
    if exempt_channels is not None and len(exempt_channels) > 50:  # noqa: PLR2004
        msg = "exempt_channels must be 50 items or fewer"
        raise ValueError(msg)


class ModerationEndpointMixin:
    @overload
    async def _api_get_guild_audit_log(
        self: "AdapterProtocol",
        bot: "Bot",
        *,
        guild_id: SnowflakeType,
        user_id: SnowflakeType | None = None,
        action_type: AuditLogEventType | None = None,
        before: SnowflakeType | None = None,
        after: None = None,
        limit: Annotated[
            int | None,
            Range(message="limit must be between 1 and 100", ge=1, le=100),
        ] = None,
    ) -> AuditLog: ...

    @overload
    async def _api_get_guild_audit_log(
        self: "AdapterProtocol",
        bot: "Bot",
        *,
        guild_id: SnowflakeType,
        user_id: SnowflakeType | None = None,
        action_type: AuditLogEventType | None = None,
        before: None = None,
        after: SnowflakeType | None = None,
        limit: Annotated[
            int | None,
            Range(message="limit must be between 1 and 100", ge=1, le=100),
        ] = None,
    ) -> AuditLog: ...

    @validate(
        cross_rules=(
            AtMostOne(
                fields=("before", "after"),
                message="before and after are mutually exclusive",
            ),
        )
    )
    async def _api_get_guild_audit_log(  # noqa: PLR0913
        self: "AdapterProtocol",
        bot: "Bot",
        *,
        guild_id: SnowflakeType,
        user_id: SnowflakeType | None = None,
        action_type: AuditLogEventType | None = None,
        before: SnowflakeType | None = None,
        after: SnowflakeType | None = None,
        limit: Annotated[
            int | None,
            Range(message="limit must be between 1 and 100", ge=1, le=100),
        ] = None,
    ) -> AuditLog:
        """Get guild audit log.

        see https://discord.com/developers/docs/resources/audit-log#get-guild-audit-log
        """

        data = {
            "user_id": user_id,
            "action_type": action_type,
            "before": before,
            "after": after,
            "limit": limit,
        }
        call = RestCall(
            method="GET",
            url=self.base_url / f"guilds/{guild_id}/audit-logs",
            response=JsonResponse(AuditLog),
            auth=BotAuth(bot.bot_info),
            query=data,
        )
        return await REST_EXCHANGE.execute(self, call)

    async def _api_list_auto_moderation_rules_for_guild(
        self: "AdapterProtocol", bot: "Bot", *, guild_id: SnowflakeType
    ) -> list[AutoModerationRule]:
        """List auto moderation rules for guild.

        see https://discord.com/developers/docs/resources/auto-moderation#list-auto-moderation-rules-for-guild
        """

        call = RestCall(
            method="GET",
            url=self.base_url / f"guilds/{guild_id}/auto-moderation/rules",
            response=JsonResponse(list[AutoModerationRule]),
            auth=BotAuth(bot.bot_info),
        )
        return await REST_EXCHANGE.execute(self, call)

    async def _api_get_auto_moderation_rule(
        self: "AdapterProtocol",
        bot: "Bot",
        *,
        guild_id: SnowflakeType,
        rule_id: SnowflakeType,
    ) -> AutoModerationRule:
        """Get auto moderation rule.

        see https://discord.com/developers/docs/resources/auto-moderation#get-auto-moderation-rule
        """

        call = RestCall(
            method="GET",
            url=self.base_url / f"guilds/{guild_id}/auto-moderation/rules/{rule_id}",
            response=JsonResponse(AutoModerationRule),
            auth=BotAuth(bot.bot_info),
        )
        return await REST_EXCHANGE.execute(self, call)

    @overload
    async def _api_create_auto_moderation_rule(
        self: "AdapterProtocol",
        bot: "Bot",
        *,
        guild_id: SnowflakeType,
        name: str,
        event_type: AutoModerationRuleEventType,
        trigger_type: Literal[TriggerType.SPAM],
        actions: list[AutoModerationAction],
        enabled: bool = ...,
        exempt_roles: Annotated[
            list[SnowflakeType],
            Range(message="exempt_roles must be 20 items or fewer", max_length=20),
        ] = ...,
        exempt_channels: Annotated[
            list[SnowflakeType],
            Range(message="exempt_channels must be 50 items or fewer", max_length=50),
        ] = ...,
        reason: str | None = None,
    ) -> AutoModerationRule: ...

    @overload
    async def _api_create_auto_moderation_rule(
        self: "AdapterProtocol",
        bot: "Bot",
        *,
        guild_id: SnowflakeType,
        name: str,
        event_type: AutoModerationRuleEventType,
        trigger_type: NonSpamTriggerType,
        actions: list[AutoModerationAction],
        trigger_metadata: TriggerMetadata,
        enabled: bool = ...,
        exempt_roles: Annotated[
            list[SnowflakeType],
            Range(message="exempt_roles must be 20 items or fewer", max_length=20),
        ] = ...,
        exempt_channels: Annotated[
            list[SnowflakeType],
            Range(message="exempt_channels must be 50 items or fewer", max_length=50),
        ] = ...,
        reason: str | None = None,
    ) -> AutoModerationRule: ...

    async def _api_create_auto_moderation_rule(
        self: "AdapterProtocol",
        bot: "Bot",
        *,
        guild_id: SnowflakeType,
        reason: str | None = None,
        **fields: Unpack[CreateAutoModerationRuleParams],
    ) -> AutoModerationRule:
        """Create auto moderation rule.

        see https://discord.com/developers/docs/resources/auto-moderation#create-auto-moderation-rule
        """
        fields = validate_outbound_value(CreateAutoModerationRuleParams, fields)
        has_trigger_metadata = "trigger_metadata" in fields
        if fields["trigger_type"] == TriggerType.SPAM:
            if has_trigger_metadata:
                msg = "trigger_metadata must be omitted for SPAM rules"
                raise ValueError(msg)
        elif not has_trigger_metadata:
            msg = "trigger_metadata is required for this trigger_type"
            raise ValueError(msg)
        exempt_roles = fields.get("exempt_roles")
        exempt_channels = fields.get("exempt_channels")
        _validate_auto_moderation_exemptions(
            exempt_roles=exempt_roles,
            exempt_channels=exempt_channels,
        )

        payload = {key: value for key, value in fields.items() if value is not None}
        call = RestCall(
            method="POST",
            url=self.base_url / f"guilds/{guild_id}/auto-moderation/rules",
            response=JsonResponse(AutoModerationRule),
            auth=BotAuth(bot.bot_info),
            body=JsonBody(payload),
            audit_reason=reason or None,
        )
        return await REST_EXCHANGE.execute(self, call)

    async def _api_modify_auto_moderation_rule(
        self: "AdapterProtocol",
        bot: "Bot",
        *,
        guild_id: SnowflakeType,
        rule_id: SnowflakeType,
        reason: str | None = None,
        **fields: Unpack[ModifyAutoModerationRuleParams],
    ) -> AutoModerationRule:
        """Modify auto moderation rule.

        see https://discord.com/developers/docs/resources/auto-moderation#modify-auto-moderation-rule
        """
        fields = validate_outbound_value(ModifyAutoModerationRuleParams, fields)
        exempt_roles = fields.get("exempt_roles")
        exempt_channels = fields.get("exempt_channels")
        _validate_auto_moderation_exemptions(
            exempt_roles=exempt_roles,
            exempt_channels=exempt_channels,
        )

        payload = {key: value for key, value in fields.items() if value is not None}
        call = RestCall(
            method="PATCH",
            url=self.base_url / f"guilds/{guild_id}/auto-moderation/rules/{rule_id}",
            response=JsonResponse(AutoModerationRule),
            auth=BotAuth(bot.bot_info),
            body=JsonBody(payload),
            audit_reason=reason or None,
        )
        return await REST_EXCHANGE.execute(self, call)

    async def _api_delete_auto_moderation_rule(
        self: "AdapterProtocol",
        bot: "Bot",
        *,
        guild_id: SnowflakeType,
        rule_id: SnowflakeType,
        reason: str | None = None,
    ) -> None:
        """Delete auto moderation rule.

        see https://discord.com/developers/docs/resources/auto-moderation#delete-auto-moderation-rule
        """

        call = RestCall(
            method="DELETE",
            url=self.base_url / f"guilds/{guild_id}/auto-moderation/rules/{rule_id}",
            response=EmptyResponse(),
            auth=BotAuth(bot.bot_info),
            audit_reason=reason or None,
        )
        await REST_EXCHANGE.execute(self, call)


__all__ = ["ModerationEndpointMixin"]
