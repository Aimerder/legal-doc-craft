"""
LegalDocCraft - 多 Agent 法律文书生成与风险审查系统
----------------------------------------------------
通过生成、审查、合规三个专职 Agent 的辩论式协作，
自动生成高质量的民事起诉状并输出量化风险报告。
"""

import json
import random
from typing import List, Dict
from dataclasses import dataclass, field


# -------------------------------
# 模拟 LLM 调用（实际部署时替换为真实 API）
# -------------------------------
def call_llm(prompt: str, role: str = "assistant") -> str:
    """
    模拟大语言模型的推理输出。
    实际项目中请替换为 openai.ChatCompletion.create 或类似接口。
    这里返回基于角色的固定文本块，以演示完整流程。
    """
    if "生成起诉状" in prompt and "事实回溯" in prompt:
        return _mock_facts_analysis()
    elif "法律要件拆解" in prompt:
        return _mock_legal_elements()
    elif "诉讼请求构建" in prompt:
        return _mock_claims()
    elif "对方律师立场" in prompt:
        return _mock_opponent_review()
    elif "程序合规检查" in prompt:
        return _mock_compliance_check()
    elif "冲突消解" in prompt:
        return _mock_conflict_resolution(prompt)
    else:
        return "基于当前信息，无额外反馈。"


def _mock_facts_analysis() -> str:
    return ("【事实回溯】\n原告张三于2024年3月1日通过银行转账向被告李四出借人民币10万元，"
            "约定月利率1%，借期6个月。被告至今未归还本金及利息，构成违约。")


def _mock_legal_elements() -> str:
    return ("【法律要件拆解】\n1. 借贷合意：有微信聊天记录与借条；\n"
            "2. 款项交付：银行转账凭证；\n"
            "3. 利息约定：未超过一年期LPR四倍（当前3.45%×4=13.8%）；\n"
            "4. 还款期限届满：2024年9月1日；\n"
            "5. 时效：未超三年诉讼时效。")


def _mock_claims() -> str:
    return ("【诉讼请求】\n1. 请求判令被告返还借款本金10万元；\n"
            "2. 请求判令被告支付自2024年9月2日起至实际清偿日止按年利率13.8%计算的逾期利息；\n"
            "3. 本案诉讼费由被告承担。")


def _mock_opponent_review() -> str:
    risks = [
        "借条签名真实性存疑，可能被鉴定为非被告笔迹。",
        "微信聊天记录中‘同意借款’的表述模糊，可能不构成明确合意。",
        "利息约定虽未超法定上限，但原告未提供催收记录，可能影响利息起算点。",
        "诉讼时效：借款到期日2024.9.1，至今未满三年，但需保留催收证据。"
    ]
    return (f"【对方律师质疑】\n{random.choice(risks)}\n"
            "此外，证据链在‘款项交付原因’上仅有转账记录，若对方抗辩为其他经济往来，"
            "则面临败诉风险。")


def _mock_compliance_check() -> str:
    issues = [
        "案由未明确：应为‘民间借贷纠纷’。",
        "管辖法院需检查：若借条未约定，应由被告住所地或合同履行地法院管辖。",
        "起诉状格式缺少‘证据清单’附件说明。"
    ]
    return "【程序合规意见】\n" + "\n".join(random.sample(issues, k=2))


def _mock_conflict_resolution(prompt: str) -> str:
    if "签名真实性" in prompt:
        return "接受审查意见，增加‘原告可申请笔迹鉴定’的预备说明。"
    elif "管辖" in prompt:
        return "采纳合规意见，将管辖修正为合同履行地（原告所在地）。"
    else:
        return "综合各方意见，将在终稿中以注释方式提示潜在风险。"


# -------------------------------
# 数据模型
# -------------------------------
@dataclass
class LegalDocument:
    facts: str = ""
    legal_analysis: str = ""
    claims: str = ""
    final_complaint: str = ""
    risk_report: str = ""
    iteration_history: List[Dict] = field(default_factory=list)


# -------------------------------
# Agent 基类与专职 Agent
# -------------------------------
class BaseAgent:
    def __init__(self, name: str, role_prompt: str):
        self.name = name
        self.role_prompt = role_prompt

    def reason(self, context: str) -> str:
        """单步推理"""
        prompt = f"{self.role_prompt}\n当前上下文：\n{context}\n请进行下一步推理。"
        return call_llm(prompt, self.name)

    def long_chain_reasoning(self, case_input: Dict, steps: List[str]) -> List[str]:
        """长链推理：依序执行多个步骤，每步输出作为下一步输入"""
        results = []
        partial_context = json.dumps(case_input, ensure_ascii=False)
        for step in steps:
            step_prompt = f"{self.role_prompt}\n当前步骤：{step}\n已有信息：\n{partial_context}"
            step_output = call_llm(step_prompt, self.name)
            results.append(f"步骤({step}): {step_output}")
            partial_context += f"\n\n{step}结果:\n{step_output}"
        return results


class GenerationAgent(BaseAgent):
    def __init__(self):
        super().__init__("生成Agent", "你是资深民事诉讼律师，依据《民法典》精确撰写起诉状。")

    def generate_initial_document(self, case_input: Dict) -> LegalDocument:
        doc = LegalDocument()
        steps = ["事实回溯", "法律要件拆解", "诉讼请求构建"]
        chain_results = self.long_chain_reasoning(case_input, steps)
        doc.facts = chain_results[0]
        doc.legal_analysis = chain_results[1]
        doc.claims = chain_results[2]
        doc.final_complaint = self._compose_complaint(doc)
        return doc

    def _compose_complaint(self, doc: LegalDocument) -> str:
        return (f"民事起诉状\n\n原告：张三\n被告：李四\n\n"
                f"事实与理由：\n{doc.facts}\n\n法律分析：\n{doc.legal_analysis}\n\n"
                f"诉讼请求：\n{doc.claims}\n\n具状人：张三\n日期：2026年5月2日")


class ReviewAgent(BaseAgent):
    def __init__(self):
        super().__init__("审查Agent", "你是被告代理律师，专注挖掘原告证据漏洞、时效、法律适用错误。")

    def adversarial_review(self, doc: LegalDocument) -> List[str]:
        review_prompt = (f"请站在被告律师角度，对以下起诉状进行严格审查，"
                         f"指出所有可攻击的薄弱环节：\n\n{doc.final_complaint}")
        response = call_llm(review_prompt, self.name)
        return [line for line in response.split("\n") if line.strip()]


class ComplianceAgent(BaseAgent):
    def __init__(self):
        super().__init__("合规Agent", "你是法院立案庭工作人员，严格检查文书格式、案由、管辖和程序要求。")

    def compliance_audit(self, doc: LegalDocument) -> List[str]:
        prompt = f"请审查以下起诉状的程序合规性（格式、案由、管辖等）：\n\n{doc.final_complaint}"
        response = call_llm(prompt, self.name)
        return [line for line in response.split("\n") if line.strip()]


# -------------------------------
# 编排 Agent（辩论与冲突消解）
# -------------------------------
class Orchestrator:
    def __init__(self, max_iterations: int = 3):
        self.max_iterations = max_iterations
        self.gen_agent = GenerationAgent()
        self.review_agent = ReviewAgent()
        self.compliance_agent = ComplianceAgent()

    def debate_and_refine(self, case_input: Dict) -> LegalDocument:
        print("=" * 60)
        print("开始法律文书生成与多Agent辩论...")

        # 1. 生成初稿
        doc = self.gen_agent.generate_initial_document(case_input)
        print("[生成Agent] 初稿完成。")
        doc.iteration_history.append({"step": "初始生成", "content": doc.final_complaint})

        # 2. 迭代辩论
        for iteration in range(1, self.max_iterations + 1):
            print(f"\n--- 第 {iteration} 轮辩论 ---")
            risks = self.review_agent.adversarial_review(doc)
            print(f"[审查Agent] 发现风险：{len(risks)} 条")
            comp_issues = self.compliance_agent.compliance_audit(doc)
            print(f"[合规Agent] 发现程序问题：{len(comp_issues)} 条")

            if not risks and not comp_issues:
                print("没有新风险，辩论收敛。")
                break

            conflict_desc = "争议点：\n" + "\n".join(risks + comp_issues)
            print("[编排Agent] 处理冲突并优化文书...")
            resolution_prompt = (f"根据以下代理意见，对起诉状进行必要修改并给出理由：\n"
                                 f"{conflict_desc}\n\n当前起诉状：\n{doc.final_complaint}")
            resolution = call_llm(resolution_prompt, "编排Agent")

            doc = self._apply_revision(doc, resolution, risks, comp_issues)
            doc.iteration_history.append({
                "step": f"第{iteration}轮修订",
                "content": doc.final_complaint,
                "risks": risks,
                "compliance": comp_issues,
                "resolution": resolution
            })

        # 3. 风险报告
        doc.risk_report = self._generate_risk_report(doc)
        print("\n====== 终稿生成完毕 ======")
        return doc

    def _apply_revision(self, doc: LegalDocument, resolution: str,
                       risks: List[str], comp_issues: List[str]) -> LegalDocument:
        # 模拟：将编排器的决策作为备注附加到文书尾部
        doc.final_complaint += (f"\n\n[修订备注（第{len(doc.iteration_history)}轮）]\n"
                                + resolution)
        return doc

    def _generate_risk_report(self, doc: LegalDocument) -> str:
        high_count = sum("笔迹" in str(h) or "时效" in str(h) for h in doc.iteration_history)
        medium_count = sum("管辖" in str(h) or "格式" in str(h) for h in doc.iteration_history)
        total = high_count + medium_count
        level = "高" if high_count > 2 else ("中" if total > 2 else "低")
        return (f"风险评级：{level}风险\n"
                f"高风险点数量：{high_count}\n"
                f"中风险点数量：{medium_count}\n"
                f"详细分析已嵌入终稿备注。")


# -------------------------------
# 主程序入口
# -------------------------------
if __name__ == "__main__":
    sample_case = {
        "原告": "张三",
        "被告": "李四",
        "借款金额": "100000元",
        "借款日期": "2024-03-01",
        "借期": "6个月",
        "月利率": "1%",
        "还款情况": "未偿还任何款项",
        "证据": ["银行转账凭证", "微信聊天记录", "借条扫描件"]
    }

    orchestrator = Orchestrator(max_iterations=3)
    final_doc = orchestrator.debate_and_refine(sample_case)

    print("\n======== 最终起诉状 ========")
    print(final_doc.final_complaint)
    print("\n======== 风险评级报告 ========")
    print(final_doc.risk_report)
    print("\n辩论历史摘要：")
    for idx, step in enumerate(final_doc.iteration_history, 1):
        print(f"{idx}. {step['step']} - 字数 {len(step['content'])}")